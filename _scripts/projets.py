#!/usr/bin/env python3
"""Génère les images WebP et les pages des projets à partir de _data/projets.yml.

Usage (depuis la racine du dépôt) : python3 _scripts/projets.py

- Les fichiers d'origine ne sont jamais modifiés ni renommés.
- Images : images/projets/<slug>/<n>-<largeur>.webp (480, 960, 1600 px max,
  jamais agrandies), plus <slug>/og.jpg (1200 px) pour le partage.
  Les métadonnées EXIF ne sont pas recopiées.
- Montages : les bandeaux texte du haut et du bas (marque, légende, téléphone)
  et les pastilles « AVANT / APRÈS / CHANTIER EN COURS » sont retirés par découpe.
- Pages : _projets/<slug>.md (front matter seulement ; le gabarit est
  _layouts/projet.html). Dimensions : _data/projets_media.yml.
"""
import os
import sys

import yaml
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIDTHS = (480, 960, 1600)
BADGE = 100  # hauteur retirée sous le bandeau pour enlever la pastille incrustée


def navy(p):
    r, g, b = p[:3]
    return r < 40 and g < 45 and b < 60


def frame(im):
    """Zone photo d'un montage : (haut, bas) sans les bandeaux bleu nuit."""
    w, h = im.size
    rows = [sum(navy(im.getpixel((x, y))) for x in range(0, w, 20)) / (w / 20) for y in range(h)]
    top = next(y for y in range(h) if rows[y] < 0.5)
    bot = next(y for y in range(h - 1, 0, -1) if rows[y] < 0.5)
    return top, bot


def split_v(im, top, bot):
    w, _ = im.size
    cols = [sum(navy(im.getpixel((x, y))) for y in range(top + 20, bot - 20, 20)) / ((bot - top - 40) / 20) for x in range(w)]
    divs = [x for x in range(w // 3, 2 * w // 3) if cols[x] > 0.5]
    return (min(divs), max(divs)) if divs else (w // 2 - 3, w // 2 + 3)


def split_h(im, top, bot):
    w, _ = im.size
    rows = [y for y in range(top + 50, bot - 50)
            if sum(navy(im.getpixel((x, y))) for x in range(0, w, 20)) / (w / 20) > 0.6]
    return (min(rows), max(rows)) if rows else ((top + bot) // 2 - 3, (top + bot) // 2 + 3)


def trim_black(im, limit=14):
    """Retire les bandes noires sur les bords (captures d'écran de téléphone)."""
    g = im.convert("L")
    w, h = g.size
    dark_row = lambda y: sum(g.getpixel((x, y)) for x in range(0, w, 8)) / len(range(0, w, 8)) < limit
    dark_col = lambda x: sum(g.getpixel((x, y)) for y in range(0, h, 8)) / len(range(0, h, 8)) < limit
    t, b, l, r = 0, h - 1, 0, w - 1
    while t < h // 4 and dark_row(t): t += 1
    while b > 3 * h // 4 and dark_row(b): b -= 1
    while l < w // 4 and dark_col(l): l += 1
    while r > 3 * w // 4 and dark_col(r): r -= 1
    return im.crop((l, t, r + 1, b + 1))


def cut(path, mode):
    im = Image.open(os.path.join(ROOT, path)).convert("RGB")
    if mode == "photo":
        return trim_black(im)
    top, bot = frame(im)
    w, _ = im.size
    if mode == "cadre":
        return im.crop((0, top + BADGE, w, bot))
    if mode in ("gauche", "droite"):
        a, b = split_v(im, top, bot)
        box = (0, top + BADGE, a, bot) if mode == "gauche" else (b + 1, top + BADGE, w, bot)
        return im.crop(box)
    if mode in ("haut", "bas"):
        a, b = split_h(im, top, bot)
        box = (0, top + BADGE, w, a) if mode == "haut" else (0, b + 1 + BADGE, w, bot)
        return im.crop(box)
    sys.exit(f"découpe inconnue : {mode}")


def main():
    projets = yaml.safe_load(open(os.path.join(ROOT, "_data", "projets.yml"), encoding="utf-8"))
    media = {}
    os.makedirs(os.path.join(ROOT, "_projets"), exist_ok=True)
    for order, p in enumerate(projets, 1):
        slug = p["slug"]
        out = os.path.join(ROOT, "images", "projets", slug)
        os.makedirs(out, exist_ok=True)
        items = []
        for n, ph in enumerate(p["photos"]):
            im = cut(ph["src"], ph["decoupe"])
            sizes = [w for w in WIDTHS if w < im.width] + [min(im.width, WIDTHS[-1])]
            sizes = sorted(set(sizes))
            for w in sizes:
                h = round(im.height * w / im.width)
                im.resize((w, h), Image.LANCZOS).save(os.path.join(out, f"{n}-{w}.webp"), "WEBP", quality=78, method=6)
            big = sizes[-1]
            items.append({"widths": sizes, "width": big, "height": round(im.height * big / im.width)})
            if n == p.get("couverture", 0):
                og = im.copy()
                og.thumbnail((1200, 1200))
                og.save(os.path.join(out, "og.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
        media[slug] = items
        fm = {
            "layout": "projet",
            "slug": slug,
            "order": order,
            "title": p["titre"],
            "seo_title": f"{p['titre']} – Réalisation | M&B Rénovation",
            "description": p["resume"],
            "image": f"/images/projets/{slug}/og.jpg",
            "permalink": f"/realisations/{slug}/",
        }
        with open(os.path.join(ROOT, "_projets", f"{slug}.md"), "w", encoding="utf-8") as f:
            f.write("---\n# Généré par _scripts/projets.py depuis _data/projets.yml : ne pas modifier à la main.\n")
            f.write(yaml.safe_dump(fm, allow_unicode=True, sort_keys=False))
            f.write("---\n")
    with open(os.path.join(ROOT, "_data", "projets_media.yml"), "w", encoding="utf-8") as f:
        f.write("# Généré par _scripts/projets.py : ne pas modifier à la main.\n")
        yaml.safe_dump(media, f, allow_unicode=True, sort_keys=False)
    print(f"{len(projets)} projets, {sum(len(v) for v in media.values())} photos")


if __name__ == "__main__":
    main()

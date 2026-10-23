#!/usr/bin/env python3
"""Images WebP et pages projets, à partir des données EXISTANTES du site.

Usage (depuis la racine du dépôt) : python3 _scripts/projets.py

Source du contenu : _data/realisations.yml (texte de main, non modifié).
Ce script n'invente aucun texte : titre et description d'une page projet
= texte alternatif de la photo dans _data/realisations.yml.

Génère (fichiers d'origine jamais modifiés ni renommés, EXIF non recopié) :
- images/webp/<chantier-N>-480|960|1200.webp : photos brutes chantier-*.jpg ;
- images/realisations/webp/<nom>-480|1080.webp : montages entiers (même image) ;
- images/projets/<slug>/<n>-<largeur>.webp : photos d'une page projet
  (moitiés avant / après des montages, découpées sous le bandeau, ou photos brutes) ;
- _data/webp_media.yml, _data/projets_media.yml : dimensions ;
- _projets/<slug>.md : une page par photo de /realisations/ (slug = nom du fichier).
"""
import os
import shutil
import sys

import yaml
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BADGE = 100  # hauteur retirée sous le bandeau pour enlever la pastille incrustée

# Photos de chaque page projet : (fichier source, découpe, étiquette).
# photo = fichier brut ; gauche/droite = moitié d'un montage côte à côte ; cadre = montage sans bandeaux.
R = "images/realisations/"
DECOUPES = {
    "avant-apres-carrelage-salle-de-bain": [("chantier-1.jpg", "photo", "avant"), ("chantier-2.jpg", "photo", "apres")],
    "avant-apres-chambre": [("chantier-9.jpg", "photo", "avant"), ("chantier-10.jpg", "photo", "apres")],
    "avant-apres-douche": [(R + "avant-apres-douche.jpg", "gauche", "avant"), (R + "avant-apres-douche.jpg", "droite", "apres")],
    "avant-apres-plafond-salle-de-bain": [(R + "avant-apres-plafond-salle-de-bain.jpg", "gauche", "avant"), (R + "avant-apres-plafond-salle-de-bain.jpg", "droite", "apres")],
    "avant-apres-salle-de-bain": [("chantier-5.jpg", "photo", "avant"), ("chantier-6.jpg", "photo", "apres")],
    "avant-apres-sejour": [("chantier-12.jpg", "photo", "avant"), ("chantier-13.jpg", "photo", "apres")],
    "avant-apres-tableau-electrique": [(R + "avant-apres-tableau-electrique.jpg", "gauche", "avant"), (R + "avant-apres-tableau-electrique.jpg", "droite", "apres")],
    "avant-pendant-piece-pierre": [(R + "avant-pendant-piece-pierre.jpg", "gauche", "avant"), (R + "avant-pendant-piece-pierre.jpg", "droite", "en-cours"), ("chantier-4.jpg", "photo", "en-cours")],
    "chantier-electricite": [(R + "chantier-electricite.jpg", "cadre", ""), ("chantier-3.jpg", "photo", "")],
    "chantier-cuisine": [(R + "chantier-cuisine.jpg", "cadre", ""), ("chantier-11.jpg", "photo", "")],
    "chantier-plafond-fissures": [(R + "chantier-plafond-fissures.jpg", "cadre", ""), ("chantier-8.jpg", "photo", "")],
    "chantier-plafonds-electricite": [(R + "chantier-plafonds-electricite.jpg", "cadre", ""), ("chantier-4.jpg", "photo", "")],
}


def navy(p):
    r, g, b = p[:3]
    return r < 40 and g < 45 and b < 60


def frame(im):
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
        return im.crop((0, top + BADGE, a, bot) if mode == "gauche" else (b + 1, top + BADGE, w, bot))
    sys.exit(f"découpe inconnue : {mode}")


def save_sizes(im, prefix, widths, quality=78):
    sizes = sorted(set([w for w in widths if w < im.width] + [min(im.width, widths[-1])]))
    for w in sizes:
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(f"{prefix}-{w}.webp", "WEBP", quality=quality, method=6)
    big = sizes[-1]
    return {"widths": sizes, "width": big, "height": round(im.height * big / im.width)}


def main():
    webp_media = {}
    # Photos brutes chantier-*.jpg (accueil, galeries Portfolio / L'Envers du Décor)
    os.makedirs(os.path.join(ROOT, "images", "webp"), exist_ok=True)
    for f in sorted(os.listdir(ROOT)):
        if f.startswith("chantier-") and f.endswith(".jpg"):
            im = Image.open(os.path.join(ROOT, f)).convert("RGB")
            webp_media[f] = dict(save_sizes(im, os.path.join(ROOT, "images", "webp", f[:-4]), (480, 960, 1200)), dir="/images/webp/")
    # Montages entiers (même image que l'original)
    src = os.path.join(ROOT, "images", "realisations")
    os.makedirs(os.path.join(src, "webp"), exist_ok=True)
    for f in sorted(os.listdir(src)):
        if f.endswith(".jpg"):
            im = Image.open(os.path.join(src, f)).convert("RGB")
            webp_media["realisations/" + f] = dict(save_sizes(im, os.path.join(src, "webp", f[:-4]), (480, 1080), 80), dir="/images/realisations/webp/")

    # Pages projets : une par photo de _data/realisations.yml
    sections = yaml.safe_load(open(os.path.join(ROOT, "_data", "realisations.yml"), encoding="utf-8"))
    shutil.rmtree(os.path.join(ROOT, "_projets"), ignore_errors=True)
    shutil.rmtree(os.path.join(ROOT, "images", "projets"), ignore_errors=True)
    os.makedirs(os.path.join(ROOT, "_projets"))
    media, order = {}, 0
    for sec in sections:
        for ph in sec["photos"]:
            order += 1
            slug = ph["file"][:-4]
            out = os.path.join(ROOT, "images", "projets", slug)
            os.makedirs(out, exist_ok=True)
            items = []
            for n, (path, mode, label) in enumerate(DECOUPES.get(slug, [(R + ph["file"], "cadre", "")])):
                m = save_sizes(cut(path, mode), os.path.join(out, str(n)), (480, 960, 1600))
                m["etiquette"] = label
                items.append(m)
            media[slug] = items
            titre = ph["alt"].replace(" – M&B Rénovation", "")
            fm = {"layout": "projet", "slug": slug, "order": order, "section": sec["title"],
                  "title": titre, "description": ph["alt"], "alt": ph["alt"],
                  "image": "/images/realisations/" + ph["file"], "permalink": f"/realisations/{slug}/"}
            with open(os.path.join(ROOT, "_projets", f"{slug}.md"), "w", encoding="utf-8") as fh:
                fh.write("---\n# Généré par _scripts/projets.py depuis _data/realisations.yml : ne pas modifier à la main.\n")
                fh.write(yaml.safe_dump(fm, allow_unicode=True, sort_keys=False))
                fh.write("---\n")
    for name, data in (("projets_media.yml", media), ("webp_media.yml", webp_media)):
        with open(os.path.join(ROOT, "_data", name), "w", encoding="utf-8") as fh:
            fh.write("# Généré par _scripts/projets.py : ne pas modifier à la main.\n")
            yaml.safe_dump(data, fh, allow_unicode=True, sort_keys=False)
    print(f"{order} pages projets, {len(webp_media)} images WebP de base")


if __name__ == "__main__":
    main()

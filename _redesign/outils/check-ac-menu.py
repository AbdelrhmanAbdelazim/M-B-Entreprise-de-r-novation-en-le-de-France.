"""Check the real Jekyll preview output; no HTTP requests or form submission."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json, sys, unicodedata

root = Path(sys.argv[1])
def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")

class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
    @property
    def ids(self):
        return [a["id"] for _, a in self.tags if "id" in a]

home = root / "apercu/ac/index.html"
doc = Document(home)
markup = home.read_text()
folded = fold(markup)
images = [a for t, a in doc.tags if t == "img"]
assert len(images) == 1 and "inspiration" in images[0]["src"], images
assert "Visuel d’inspiration" in markup or "Visuel d'inspiration" in markup
assert not any(x in markup.lower() for x in ["wa.me", "fa-whatsapp", "whatsapp"])
assert "contact prive" not in folded, "Contact Privé must not appear in A-C DOM"
assert not any(x in folded for x in ["3 000", "3000 €", "3000€", "3 fois", "sans frais", "remise sur devis"]), "Old or unconfirmed financial terms must not appear in A-C"
assert "le perimetre des travaux, le prix et l'echeancier des paiements par etapes sont definis apres la visite technique et precises dans votre devis detaille." in folded.replace("’", "'"), "Missing approved payment & scope statement"
assert "paiement par etapes" in folded and "paiements selon l'avancement des travaux" in folded.replace("’", "'"), "Missing Paiement par étapes / Paiements selon l’avancement des travaux"
for phrase in [
    "peinture, finitions et sols selon les besoins",
    "perimetre defini apres examen des lieux",
    "coordination et realisation des etapes de renovation",
    "parlons de votre projet"
]:
    assert phrase in folded, f"Missing approved project entry phrase: {phrase}"
assert markup.count("Parlons de votre projet") == 3, "Each of the 3 project entry cards must have CTA 'Parlons de votre projet'"
assert "devisModal" not in doc.ids, "Parallel devisModal must not exist on A-C"
assert "var SANS_ENVOI = true;" in markup
assert len(doc.ids) == len(set(doc.ids)), "duplicate ids"
for req_id in ["mobileMenu", "pourquoi", "formules", "realisations", "portfolio", "chantiers", "processus", "avantages", "contact", "contactForm", "c-type"]:
    assert req_id in doc.ids, f"missing required id: {req_id}"
assert any(t == "dialog" and a.get("id") == "mobileMenu" for t, a in doc.tags)
assert any(t == "button" and a.get("id") == "menuBtn" and a.get("aria-controls") == "mobileMenu" for t, a in doc.tags)
# Every local destination and anchor on the homepage must actually exist.
checked = 0
for tag, attrs in doc.tags:
    if tag != "a" or not attrs.get("href"):
        continue
    link = urlsplit(attrs["href"])
    if link.scheme or link.netloc:
        continue
    path = unquote(link.path)
    target = home if not path or path == "/apercu/ac/" else root / path.lstrip("/")
    candidates = [target / "index.html", target.with_suffix(".html"), target] if target != home else [home]
    target = next((p for p in candidates if p.is_file()), None)
    assert target is not None, attrs["href"]
    if link.fragment:
        assert unquote(link.fragment) in Document(target).ids, attrs["href"]
    checked += 1

# Verify phone, email, and social links in <body> on A-C exist ONLY inside #contact
body_start = markup.index("<body")
contact_start = markup.index('id="contact"')
before_contact = markup[body_start:contact_start]
after_contact = markup[markup.index("</section>", contact_start):]
outside_contact = before_contact + after_contact
assert 'href="tel:' not in outside_contact, "tel: link found outside #contact on A-C"
assert 'href="mailto:' not in outside_contact, "mailto: link found outside #contact on A-C"

gallery_path = root / "realisations/index.html"
gallery = Document(gallery_path)
gallery_markup = gallery_path.read_text()
assert "contact prive" not in fold(gallery_markup), "Contact Privé must not appear on preview realisations page"
assert "portfolio" in gallery.ids and "chantiers" in gallery.ids
assert "avant-apres" in gallery.ids and "realisations-terminees" in gallery.ids and "sur-le-chantier" in gallery.ids
gallery_imgs = [a for t, a in gallery.tags if t == "img"]
gallery_project_imgs = [a for a in gallery_imgs if a.get("src")]
gallery_lightbox_imgs = [a for a in gallery_imgs if not a.get("src")]
assert len(gallery_imgs) == 41, len(gallery_imgs)
assert len(gallery_project_imgs) == 40 and len(gallery_lightbox_imgs) == 1, (len(gallery_project_imgs), len(gallery_lightbox_imgs))
for img in gallery_project_imgs:
    src = img.get("src", "")
    assert src and (root / src.lstrip("/")).is_file(), f"missing gallery img src: {src}"
    for part in img.get("srcset", "").split(","):
        part = part.strip()
        if part:
            u = part.split()[0]
            assert (root / u.lstrip("/")).is_file(), f"missing gallery srcset file: {u}"
assert "Contactez-nous" in markup, "missing Contactez-nous link"
for social_url in [
    "https://www.facebook.com/1028887100297504",
    "https://www.instagram.com/abdelrhman.08/",
    "https://g.page/r/CYV1sjt85bCkEBI/review",
    "https://pin.it/6WHDNJlqj",
]:
    assert social_url in markup, f"missing social URL on A-C: {social_url}"
    if social_url != "https://g.page/r/CYV1sjt85bCkEBI/review":
        assert social_url not in outside_contact, f"social URL duplicated outside #contact: {social_url}"
for direction in ["a", "b", "c"]:
    old = Document(root / f"apercu/{direction}/index.html")
    assert not any(t == "dialog" and a.get("id") == "mobileMenu" for t, a in old.tags), direction
    assert len([1 for t, _ in old.tags if t == "img"]) > 10, direction
print(json.dumps({
    "status": "passed",
    "homepage_images": len(images),
    "local_links_and_anchors_checked": checked,
    "contact_prive_occurrences": 0,
    "unified_contact_only": True,
    "parallel_devis_modal": False,
    "pourquoi_section": True,
    "formules_section": True,
    "modalites_paiement_neutral": True,
    "gallery_total_img_tags": len(gallery_imgs),
    "gallery_real_project_photos_verified_on_disk": len(gallery_project_imgs),
    "lightbox_placeholder_img": len(gallery_lightbox_imgs),
    "social_links_in_contact": 4,
    "original_previews_preserved": ["a", "b", "c"],
    "preview_form": "disabled"
}, ensure_ascii=False, indent=2))

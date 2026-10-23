"""Check the real Jekyll preview output; no HTTP requests or form submission."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json, sys

root = Path(sys.argv[1])
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
images = [a for t, a in doc.tags if t == "img"]
assert len(images) == 1 and "inspiration" in images[0]["src"], images
assert "Visuel d’inspiration" in markup or "Visuel d'inspiration" in markup
assert not any(x in markup.lower() for x in ["wa.me", "fa-whatsapp", "whatsapp"])
assert "var SANS_ENVOI = true;" in markup
assert len(doc.ids) == len(set(doc.ids)), "duplicate ids"
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
    target = home if not path else root / path.lstrip("/")
    candidates = [target / "index.html", target.with_suffix(".html"), target] if target != home else [home]
    target = next((p for p in candidates if p.is_file()), None)
    assert target is not None, attrs["href"]
    if link.fragment:
        assert unquote(link.fragment) in Document(target).ids, attrs["href"]
    checked += 1
gallery = Document(root / "realisations/index.html")
assert "portfolio" in gallery.ids and "chantiers" in gallery.ids
assert len([1 for t, _ in gallery.tags if t == "img"]) > 20
for direction in ["a", "b", "c"]:
    old = Document(root / f"apercu/{direction}/index.html")
    assert not any(t == "dialog" and a.get("id") == "mobileMenu" for t, a in old.tags), direction
    assert len([1 for t, _ in old.tags if t == "img"]) > 10, direction
print(json.dumps({"status": "passed", "homepage_images": len(images), "local_links_and_anchors_checked": checked, "gallery_images": len([1 for t, _ in gallery.tags if t == "img"]), "original_previews_preserved": ["a", "b", "c"], "preview_form": "disabled"}, ensure_ascii=False, indent=2))

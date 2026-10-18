"""Rebuild index.html (read-only snapshot) from src/live-map.html, src/verdania-map.jpg and pins.json.

Usage: python3 build.py
pins.json is a list of pin objects: {id, name, kind (visited|lead|note), notes, x, y (percent), approx, order}.
"""
import base64, io, json, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
LIVE_URL = "https://claude.ai/artifact/AZj3DdH1RZEdNjSZx89h6U"

src = (ROOT / "src/live-map.html").read_text()
pins = json.loads((ROOT / "pins.json").read_text())
for p in pins:
    p.pop("updated", None)

im = Image.open(ROOT / "src/verdania-map.jpg").convert("RGB")
buf = io.BytesIO(); im.save(buf, "JPEG", quality=80, optimize=True, progressive=True)
uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

reps = [
    ('src="verdania-map.jpg"', f'src="{uri}"'),
    ('<button id="addBtn" class="primary" aria-pressed="false" type="button">＋ Add pin</button>',
     f'<a class="btn primary" href="{LIVE_URL}" target="_blank" rel="noopener" style="text-decoration:none">Open live map ↗</a><button id="addBtn" hidden type="button">Add</button>'),
    ("try{ const z=parseFloat", "S.pins=" + json.dumps(pins).replace("</", "<\\/") + "; S.canWrite=false; S.loaded=true;\ntry{ const z=parseFloat"),
    ("Pins added in this view aren't saved. Open the published page to keep them.",
     "This is a read-only snapshot. Use “Open live map” to add, move or edit pins."),
    ("Dashed pins mark approximate spots.", "Snapshot of the live map. Dashed pins mark approximate spots."),
]
for a, b in reps:
    assert src.count(a) == 1, f"build marker not found exactly once: {a[:50]}"
    src = src.replace(a, b)

doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">'
       + src + "</body></html>")
(ROOT / "index.html").write_text(doc)
print(f"index.html: {len(doc.encode())} bytes, {len(pins)} pins")

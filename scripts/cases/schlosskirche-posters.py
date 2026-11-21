# The posters slide in the Schlosskirche project drawer (src/assets/work/schlosskirche-posters.png,
# 2880x1800): three A1 posters from the "Kirche anders" services (2017), side by side as sheets
# with a soft shadow on light grey.
# Sources: the print PDFs in the Schloßkirche folder (01_Kirche anders/05_Production/2017/
# Plakat A1), rendered to PNG 3000px tall with sips and kept in
# "03_Working files/schlosskirche-posters/".
# Usage: python3 scripts/cases/schlosskirche-posters.py   (from rco-website/, needs Pillow)
from pathlib import Path
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT.parent / "03_Working files/schlosskirche-posters"
OUT = ROOT / "src/assets/work/schlosskirche-posters.png"
W, H, BG = 2880, 1800, (226, 224, 220)
POSTERS = ["domicile", "hauptbahnhof", "kommunales-kino"]
PH, GAP, SHADOW = 1120, 110, 80

sheets = []
for name in POSTERS:
    im = Image.open(SRC / f"poster-{name}.png").convert("RGB")
    sheets.append(im.resize((round(im.width * PH / im.height), PH), Image.LANCZOS))

total = sum(s.width for s in sheets) + GAP * (len(sheets) - 1)
x, y = (W - total) // 2, (H - PH) // 2
canvas = Image.new("RGB", (W, H), BG)
shadow = Image.new("L", (W, H), 0)
spots = []
for s in sheets:
    shadow.paste(SHADOW, (x, y + 20, x + s.width, y + 20 + PH))
    spots.append((s, x))
    x += s.width + GAP
canvas.paste((0, 0, 0), (0, 0), shadow.filter(ImageFilter.GaussianBlur(36)))
for s, sx in spots:
    canvas.paste(s, (sx, y))
canvas.save(OUT, optimize=True)
print(OUT, canvas.size, "posters", sheets[0].size)

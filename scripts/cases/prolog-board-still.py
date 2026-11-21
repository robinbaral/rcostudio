# A still image of ProLog's page concepts board (src/assets/work/prolog-page-concepts.png,
# 2880x1800), for the hover preview and its thumbnails. The drawer shows the live board
# (CaseBoard, settings in src/data/projects.ts); this follows its layout: three pages in a row on
# the light board colour, 5% padding at the top and sides, a 3.1% gap, the middle page 3.75%
# lower, each cut from the top and running off the bottom edge (here at 16:10).
# Usage: python3 scripts/cases/prolog-board-still.py   (from rco-website/, needs Pillow)
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src/assets/cases/prolog/boards/prolog-page-concepts"
OUT = ROOT / "src/assets/work/prolog-page-concepts.png"
W, H, BG = 2880, 1800, (242, 241, 238)  # --board, light mode (global.css)
PAD, GAP, DROPS = 5, 3.1, [0, 3.75, 0]

pages = [Image.open(p).convert("RGB") for p in sorted(SRC.glob("*.png"))]
pw = (W * (1 - 2 * PAD / 100) - W * GAP / 100 * (len(pages) - 1)) / len(pages)
canvas = Image.new("RGB", (W, H), BG)
x = W * PAD / 100
for page, drop in zip(pages, DROPS):
    page = page.resize((round(pw), round(page.height * pw / page.width)), Image.LANCZOS)
    y = round(W * PAD / 100 + W * drop / 100)
    canvas.paste(page.crop((0, 0, page.width, H - y)), (round(x), y))
    x += pw + W * GAP / 100
canvas.save(OUT, optimize=True)
print(OUT, canvas.size, "page width", round(pw))

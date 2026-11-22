# Slides for two older projects (Banking App, QuickScan) in the project
# drawer (src/assets/work/<project>-<n>.png, 2880x1800), from Robin's Behance boards
# (2800px wide, saved in "03_Working files/behance/<project>/"). Each board is brought to 16:10:
# a wider one is extended above and below in its own edge colour, a taller one is cropped
# (centred, or from the top where the board's title sits there). Banking App's other slides
# come from the phone renders, in bank-renders.py.
# Usage: python3 scripts/cases/behance-slides.py   (from rco-website/, needs Pillow)
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT.parent / "03_Working files/behance"
OUT = ROOT / "src/assets/work"
W, H = 2880, 1800

# (project folder, source number or file name, output name, crop anchor for tall boards: 0 top … 1 bottom)
# QuickScan's hero and its next two slides (multi-page, phone in hand) are Robin's own 16:10
# exports ("Tile – 3.png", "custom – 21.png", "custom – 20.png"), resized by hand, not made here.
SLIDES = [
    ("banking", 1, "banking-app-hero", 0.5),
    ("banking", 7, "banking-app-transfers", 0.5),
    ("quickscan", 5, "quickscan-flow", 0.5),
    ("quickscan", 6, "quickscan-screens", 0.5),
]


def to_16_10(img, anchor):
    w, h = img.size
    target_h = round(w * 10 / 16)
    if h >= target_h:  # taller: crop
        top = round((h - target_h) * anchor)
        return img.crop((0, top, w, top + target_h))
    # wider: extend above and below with the colours of its top and bottom rows
    out = Image.new("RGB", (w, target_h))
    pad = (target_h - h) // 2
    out.paste(img.crop((0, 0, w, 1)).resize((w, pad)), (0, 0))
    out.paste(img.crop((0, h - 1, w, h)).resize((w, target_h - h - pad)), (0, pad + h))
    out.paste(img, (0, pad))
    return out


for folder, n, name, anchor in SLIDES:
    src = n if isinstance(n, str) else f"{n:02d}.png"
    img = Image.open(SRC / folder / src).convert("RGB")
    out = to_16_10(img, anchor).resize((W, H), Image.LANCZOS)
    out.save(OUT / f"{name}.png", optimize=True)
    print(name, img.size, "->", out.size)

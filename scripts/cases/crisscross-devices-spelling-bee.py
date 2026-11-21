# The iPad and iPhone slide in the CrissCross project drawer (src/assets/work/crisscross-devices-1.png,
# 2880x1800): a puzzle on an 11-inch iPad in landscape with a puzzle on an iPhone overlapping its
# right edge, both in the Spelling Bee theme, as rounded screens with soft shadows on white.
# Sizes and corner radii are measured from the earlier version of the slide.
# Sources: "03_Working files/crisscross-devices-spelling-bee/" (Simulator captures, 2026-11-22:
# iPad Pro 11-inch, the Daily Puzzle; iPhone 18 Pro, Jobs 1 from the Starter pack).
# Usage: python3 scripts/cases/crisscross-devices-spelling-bee.py   (from rco-website/, needs Pillow, numpy)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT.parent / "03_Working files/crisscross-devices-spelling-bee"
OUT = ROOT / "src/assets/work/crisscross-devices-1.png"
W, H, BG = 2880, 1800, (255, 255, 255)
# (file, left, top, width, corner radius), back to front; the pair is centred on the slide
# (iPad left edge to iPhone right edge, iPad top to iPhone bottom).
SCREENS = [("ipad-puzzle.png", 260, 181, 2001, 61), ("iphone-puzzle.png", 1991, 251, 629, 92)]
SHADOW_BLUR, SHADOW_DY, SHADOW_ALPHA = 60, 30, 0.21


def rounded(img, w, r):
    h = round(w * img.height / img.width)
    mask = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w * 4 - 1, h * 4 - 1), r * 4, fill=255)
    out = img.convert("RGB").resize((w, h), Image.LANCZOS).convert("RGBA")
    out.putalpha(mask.resize((w, h), Image.LANCZOS))
    return out


canvas = Image.new("RGB", (W, H), BG)
for name, x, y, w, r in SCREENS:
    screen = rounded(Image.open(SRC / name), w, r)
    sh = Image.new("L", (W, H), 0)
    sh.paste(screen.getchannel("A"), (x, y + SHADOW_DY), screen.getchannel("A"))
    b = np.array(sh.filter(ImageFilter.GaussianBlur(SHADOW_BLUR)), dtype=float)[..., None] / 255
    canvas = Image.fromarray((np.array(canvas, dtype=float) * (1 - SHADOW_ALPHA * b)).round().astype(np.uint8))
    canvas.paste(screen, (x, y), screen)
    print(name, "at", (x, y), "size", screen.size)
canvas.save(OUT, optimize=True)
print(OUT)

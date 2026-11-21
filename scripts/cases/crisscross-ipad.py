# The iPad slide in the CrissCross project drawer (src/assets/work/crisscross-devices-2.png,
# 2880x1800): a landscape iPad mini screenshot as a rounded screen with a soft shadow on light
# grey. Background, corner radius and shadow are measured from the earlier version of the slide;
# the screen keeps its width and takes the screenshot's own proportions, centred.
# Source: "03_Working files/crisscross-ipad/ipad-mini-home.png" (Simulator, 2026-11-15).
# Usage: python3 scripts/cases/crisscross-ipad.py   (from rco-website/, needs Pillow and numpy)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT.parent / "03_Working files/crisscross-ipad/ipad-mini-home.png"
OUT = ROOT / "src/assets/work/crisscross-devices-2.png"
W, H, BG = 2880, 1800, (246, 246, 244)
SCREEN_W, RADIUS = 2118, 64
SHADOW_BLUR, SHADOW_DY, SHADOW_ALPHA = 60, 30, 0.214

shot = Image.open(SRC).convert("RGB")
sw, sh = SCREEN_W, round(SCREEN_W * shot.height / shot.width)
x0, y0 = (W - sw) // 2, (H - sh) // 2
shot = shot.resize((sw, sh), Image.LANCZOS)

shadow = Image.new("L", (W, H), 0)
ImageDraw.Draw(shadow).rounded_rectangle((x0, y0 + SHADOW_DY, x0 + sw - 1, y0 + sh - 1 + SHADOW_DY), RADIUS, fill=255)
b = np.array(shadow.filter(ImageFilter.GaussianBlur(SHADOW_BLUR)), dtype=float)[..., None] / 255
board = Image.fromarray((np.array(BG, dtype=float) * (1 - SHADOW_ALPHA * b)).round().astype(np.uint8))

# Rounded corners, drawn at 4x and scaled down for a smooth edge.
mask = Image.new("L", (sw * 4, sh * 4), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw * 4 - 1, sh * 4 - 1), RADIUS * 4, fill=255)
board.paste(shot, (x0, y0), mask.resize((sw, sh), Image.LANCZOS))
board.save(OUT, optimize=True)
print(OUT, board.size, "screen", (x0, y0, sw, sh))

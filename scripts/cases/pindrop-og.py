# Pindrop's preview slide (src/assets/work/pindrop-og.png, 2880x1800): the logo lockup and the
# phone from the OG image in Figma "Pindrop Screens" (node 6:2), laid out for 16:10. The lockup
# sits in the vertical centre; the phone stands to its right, its top 300px down, running off
# the bottom edge; the pair has the same margin left and right.
# Sources, in "03_Working files/pindrop-og-layers/": the phone mock-up (raw-a.png, the full
# phone from the Figma layer's image fill, transparent around it) and the lockup, icon with its
# shadow and wordmark (lockup-from-slide.png, cut from the earlier slide on this same grey).
# Usage: python3 scripts/cases/pindrop-og.py   (from rco-website/, needs Pillow)
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT.parent / "03_Working files/pindrop-og-layers"
OUT = ROOT / "src/assets/work/pindrop-og.png"
W, H, BG = 2880, 1800, (246, 246, 244)
PHONE_W, PHONE_TOP, GAP = 1006, 300, 302  # phone body width, its top, lockup to phone

lockup = Image.open(SRC / "lockup-from-slide.png").convert("RGB")
# The lockup's own content inside that cut: icon left edge to wordmark right edge, top to bottom
# of the icon (the rest is its shadow and the grey around it).
LX0, LX1, LY0, LY1 = 53, 1081, 76, 359

raw = Image.open(SRC / "raw-a.png").convert("RGBA")
bx0, by0, bx1, by1 = raw.getbbox()  # the phone body, without the transparent margin
k = PHONE_W / (bx1 - bx0)
phone = raw.resize((round(raw.width * k), round(raw.height * k)), Image.LANCZOS)
px0, py0 = round(bx0 * k), round(by0 * k)

total = (LX1 - LX0) + GAP + PHONE_W
left = (W - total) // 2
canvas = Image.new("RGB", (W, H), BG)
canvas.paste(lockup, (left - LX0, round(H / 2 - (LY0 + LY1) / 2)))
canvas.paste(phone, (left + (LX1 - LX0) + GAP - px0, PHONE_TOP - py0), phone)
canvas.save(OUT, optimize=True)
print(OUT, "margins", left, W - left - total)

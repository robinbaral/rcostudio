# The achievements slide in the CrissCross project drawer (src/assets/work/crisscross-achievements.png,
# 2880x1800): three achievement cards cut from iPad Pro simulator screenshots, side by side and
# overlapping, the middle one larger and in front, with soft shadows on white. The app's back
# button is painted out of each card.
# Sources: "03_Working files/crisscross-achievements/" (Simulator, 2026-11-22). Each card sits at
# the same place on the screen: 1160x1318 at (630, 175), corners rounded at 64px.
# Usage: python3 scripts/cases/crisscross-achievements.py   (from rco-website/, needs Pillow)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT.parent / "03_Working files/crisscross-achievements"
OUT = ROOT / "src/assets/work/crisscross-achievements.png"
W, H, BG = 2880, 1800, (255, 255, 255)
# Inset by 2px so no edge pixel of the dimmed screen behind comes along.
CARD, RADIUS = (632, 177, 1788, 1491), 62
FRONT_H, BACK_H, OVERLAP = 1160, 890, 140
# The app's back button in each card's top-left corner (crop coordinates), painted out.
BUTTON = (12, 11, 110, 109)


def card(name, h):
    shot = Image.open(SRC / f"{name}.png").convert("RGB").crop(CARD)
    ImageDraw.Draw(shot).ellipse(BUTTON, fill=shot.getpixel((68, 900)))
    w = round(shot.width * h / shot.height)
    r = round(RADIUS * h / shot.height)
    # Rounded corners drawn at 4x and scaled down for a smooth edge.
    mask = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w * 4 - 1, h * 4 - 1), r * 4, fill=255)
    out = shot.resize((w, h), Image.LANCZOS).convert("RGBA")
    out.putalpha(mask.resize((w, h), Image.LANCZOS))
    return out


front = card("crossword-curious", FRONT_H)
left, right = card("word-up", BACK_H), card("medal-collector", BACK_H)
fx, fy = (W - front.width) // 2, (H - front.height) // 2
by = (H - BACK_H) // 2
spots = [(left, fx + OVERLAP - left.width, by), (right, fx + front.width - OVERLAP, by), (front, fx, fy)]

canvas = Image.new("RGB", (W, H), BG)
for img, x, y in spots:  # back to front, each with its own shadow so the front one falls on the others
    sh = Image.new("L", (W, H), 0)
    sh.paste(img.getchannel("A").point(lambda v: v * 0.28), (x, y + 30), img.getchannel("A"))
    canvas.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(45)))
    canvas.paste(img, (x, y), img)
canvas.save(OUT, optimize=True)
print(OUT, canvas.size, "front", front.size, "back", left.size, "x", [s[1] for s in spots])

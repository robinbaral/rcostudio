# Pindrop boards for the project drawer and the hero stack (src/assets/work/pindrop-*.png,
# 2880x1800), from the plain iPhone 17 Pro screenshots in Figma "Pindrop Screens" (file
# tX7ot5BuFwtsVaYjEb7TF4, page "Version 1.5", nodes 16:34 to 16:39), kept in
# "03_Working files/pindrop-screens/". Each screen is drawn as a phone (rounded corners, thin
# black bezel, soft shadow), three side by side.
# - screens-1: score drag, onboarding, players (light, dark, light).
# - screens-2: dark mode, "down to 25", the win (dark, light, dark).
# - hero: score drag, dark mode, players on the app's red, a card for the homepage hero stack
#   (the red "down to 25" screen would disappear into it).
# Usage: python3 scripts/cases/pindrop-boards.py   (from rco-website/)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT.parent / "03_Working files/pindrop-screens"
OUT = ROOT / "src/assets/work"
W, H, BG = 2880, 1800, (242, 241, 238)


def phone(n, h):
    """Screen n as a phone h pixels tall: the screen inside a 2.4% black bezel, both rounded."""
    shot = Image.open(SRC / f"pindrop-screen-{n}.png").convert("RGB")
    bezel = round(h * 0.024)
    sh = h - 2 * bezel
    sw = round(shot.width * sh / shot.height)
    w = sw + 2 * bezel
    r_out, r_in = round(w * 0.16), round(sw * 0.145)
    body = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(body).rounded_rectangle((0, 0, w - 1, h - 1), r_out, fill=(20, 20, 20, 255))
    screen = shot.resize((sw, sh), Image.LANCZOS)
    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, sh - 1), r_in, fill=255)
    body.paste(screen, (bezel, bezel), mask)
    return body


def board(screens, name, bg, ph=1440, gap=150, shadow=70):
    phones = [phone(n, ph) for n in screens]
    total = sum(p.width for p in phones) + gap * (len(phones) - 1)
    x, y = (W - total) // 2, (H - ph) // 2
    canvas = Image.new("RGB", (W, H), bg)
    sh = Image.new("L", (W, H), 0)
    spots = []
    for p in phones:
        sh.paste(p.getchannel("A").point(lambda v: shadow if v else 0), (x, y + 24), p.getchannel("A"))
        spots.append((p, x))
        x += p.width + gap
    canvas.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(40)))
    for p, px in spots:
        canvas.paste(p, (px, y), p)
    canvas.save(OUT / f"pindrop-{name}.png")
    print(name, canvas.size)


RED = Image.open(SRC / "pindrop-screen-5.png").convert("RGB").getpixel((603, 1250))
board([1, 2, 3], "screens-1", BG)
board([4, 5, 6], "screens-2", BG)
board([1, 4, 3], "hero", RED, shadow=90)

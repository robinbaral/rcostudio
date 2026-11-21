# The themes slide in the Faster project drawer (src/assets/work/faster-themes.png, 2880x1800):
# the timer in all five themes (Minimal, Night, Default, Full Phase, Pop), each once, as phones
# of one size in a row with even gaps and no overlaps, nudged down and up in turn. On the light
# grey of Faster's other boards.
# Sources: the App Store captures in ~/Projects/Faster/faster-app/design/screenshots/raw/
# (timer-*.png, 1206x2622, iPhone 17 Pro). They have no Dynamic Island, so one is drawn in.
# Usage: python3 scripts/cases/faster-themes.py   (from rco-website/, needs Pillow)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
SRC = Path.home() / "Projects/Faster/faster-app/design/screenshots/raw"
OUT = ROOT / "src/assets/work/faster-themes.png"
W, H, BG = 2880, 1800, (245, 245, 247)
SS = 3  # shapes drawn at 3x for smooth edges

# Left to right, Default in the middle.
THEMES = ["timer-minimal", "timer-night", "timer-default", "timer-phaseColor", "timer-pop"]
PHONE_H, GAP, STAGGER = 860, 90, 110  # phone height; gap between phones, across and down


def phone(name, h):
    """The screen inside a thin black bezel, both rounded, with a Dynamic Island."""
    shot = Image.open(SRC / f"{name}.png").convert("RGB")
    bezel = round(h * 0.022)
    sh = h - 2 * bezel
    sw = round(shot.width * sh / shot.height)
    w = sw + 2 * bezel
    r_out, r_in = round(w * 0.155), round(sw * 0.14)
    body = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    ImageDraw.Draw(body).rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), r_out * SS, fill=(18, 18, 18, 255))
    body = body.resize((w, h), Image.LANCZOS)
    mask = Image.new("L", (sw * SS, sh * SS), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw * SS - 1, sh * SS - 1), r_in * SS, fill=255)
    body.paste(shot.resize((sw, sh), Image.LANCZOS), (bezel, bezel), mask.resize((sw, sh), Image.LANCZOS))
    # Dynamic Island: 125x37 pt, 11 pt from the top, on a 402 pt wide screen.
    iw, ih, it = sw * 125 / 402, sw * 37 / 402, sw * 11 / 402
    pill = Image.new("L", (round(iw * SS), round(ih * SS)), 0)
    ImageDraw.Draw(pill).rounded_rectangle((0, 0, pill.width - 1, pill.height - 1), pill.height // 2, fill=255)
    pill = pill.resize((round(iw), round(ih)), Image.LANCZOS)
    body.paste((0, 0, 0, 255), (round(bezel + (sw - iw) / 2), round(bezel + it)), pill)
    return body


phones = [phone(name, PHONE_H) for name in THEMES]
pw = phones[0].width
left = (W - (len(THEMES) * pw + (len(THEMES) - 1) * GAP)) // 2
canvas = Image.new("RGB", (W, H), BG)
shadow = Image.new("L", (W, H), 0)
spots = []
for col, p in enumerate(phones):
    x = left + col * (pw + GAP)
    # Each theme once: the first, middle and last a little lower, the two between a little higher.
    y = (H - PHONE_H) // 2 + (STAGGER if col % 2 == 0 else -STAGGER)
    shadow.paste(p.getchannel("A").point(lambda v: v * 0.22), (x, y + 24), p.getchannel("A"))
    spots.append((p, x, y))
canvas.paste((0, 0, 0), (0, 0), shadow.filter(ImageFilter.GaussianBlur(40)))
for p, x, y in spots:
    canvas.paste(p, (x, y), p)
canvas.save(OUT, optimize=True)
print(OUT, "phone", (pw, PHONE_H), "side margin", left)

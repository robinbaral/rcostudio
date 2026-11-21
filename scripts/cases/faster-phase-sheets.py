# The phases slide in the Faster project drawer (src/assets/work/faster-phases.png, 2880x1800):
# the five phase sheets (Digesting, Settling, Fat Burning, Ketosis, Deep Fast) open over the
# timer, as full phones in a row along the middle, with even gaps between them and around them. On the light grey of Faster's other boards.
# Sources: "03_Working files/faster-phase-sheets/" (iPhone 17 Pro simulator, a fast 13 hours
# in, 2026-11-22). The captures have no Dynamic Island, so one is drawn in.
# Usage: python3 scripts/cases/faster-phase-sheets.py   (from rco-website/, needs Pillow)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT.parent / "03_Working files/faster-phase-sheets"
OUT = ROOT / "src/assets/work/faster-phases.png"
W, H, BG = 2880, 1800, (245, 245, 247)
SS = 3  # shapes drawn at 3x for smooth edges
PHONE_H, OVERLAP = 940, -90  # a negative overlap is the gap between phones
NUDGES = [0, 0, 0, 0, 0]


def phone(path, h):
    """The screen inside a thin black bezel, both rounded (as on the themes slide)."""
    shot = Image.open(path).convert("RGB")
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


phones = [phone(p, PHONE_H) for p in sorted(SRC.glob("*.png"))]
total = sum(p.width for p in phones) - OVERLAP * (len(phones) - 1)
x = (W - total) // 2
canvas = Image.new("RGB", (W, H), BG)
for p, nudge in zip(phones, NUDGES):  # left to right
    y = (H - PHONE_H) // 2 + nudge
    sh = Image.new("L", (W, H), 0)
    sh.paste(p.getchannel("A").point(lambda v: v * 0.26), (x, y + 26), p.getchannel("A"))
    canvas.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(44)))
    canvas.paste(p, (x, y), p)
    x += p.width - OVERLAP
canvas.save(OUT, optimize=True)
print(OUT, "phone", phones[0].size, "row", total)

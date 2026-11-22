# The Pop Drop project's two images (src/assets/work/pop-drop-*.png, 2880x1800 each):
# - pop-drop-header.png: the App Store header at 16:10 in Figma "Pop Drop" (page "App Store",
#   frame 47:3585, 3840x2400): Robin's arrangement, balls up both sides of the title. Scaled
#   down to 2880x1800.
# - pop-drop-themes.png: the game in its five light themes (Playground, Sunset, Autumn, Picnic,
#   Beach), as phones of one size in a row, nudged down and up in turn, on the header's warm grey.
#   Same layout as faster-themes.py.
# The store screenshots and the iPhone Duo mock-ups stay out (Robin, 2026-11-22).
# Sources: the header export in 01_Website/03_Working files/pop-drop/ and the App Store
# captures in ~/Projects/Pop Drop/pop-drop-app/docs/screenshots/20-app-store/ (1206x2622).
# Usage: python3 scripts/cases/pop-drop-slides.py   (from rco-website/, needs Pillow)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
FIGMA = ROOT.parent / "03_Working files/pop-drop"
SHOTS = Path.home() / "Projects/Pop Drop/pop-drop-app/docs/screenshots/20-app-store"
OUT = ROOT / "src/assets/work"
W, H = 2880, 1800
SS = 3  # shapes drawn at 3x for smooth edges


def cover(img):
    """Scale to fill W x H and crop the middle."""
    k = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)
    x, y = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((x, y, x + W, y + H))


# Header
header = Image.open(FIGMA / "figma-header-16x10-47-3585.png").convert("RGB")
BG = header.getpixel((header.width // 2, 20))  # the warm grey behind the balls
cover(header).save(OUT / "pop-drop-header.png", optimize=True)

# Themes
THEMES = ["1-playground-light", "2-sunset-light", "3-autumn-light", "4-picnic-light", "5-beach-light"]
PHONE_H, GAP, STAGGER = 860, 90, 110  # phone height; gap between phones, across and down


def phone(name, h):
    """The screen inside a thin black bezel, both rounded, with a Dynamic Island drawn in (the
    simulator captures have none), as in faster-themes.py."""
    shot = Image.open(SHOTS / f"{name}.png").convert("RGB")
    bezel = round(h * 0.022)
    sh = h - 2 * bezel
    sw = round(shot.width * sh / shot.height)
    w = sw + 2 * bezel
    # Concentric corners: the outer radius is the screen's plus the bezel, so the bezel keeps
    # its width around the corners.
    r_in = round(sw * 0.14)
    r_out = r_in + bezel
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
    y = (H - PHONE_H) // 2 + (STAGGER if col % 2 == 0 else -STAGGER)
    shadow.paste(p.getchannel("A").point(lambda v: v * 0.22), (x, y + 24), p.getchannel("A"))
    spots.append((p, x, y))
canvas.paste((0, 0, 0), (0, 0), shadow.filter(ImageFilter.GaussianBlur(40)))
for p, x, y in spots:
    canvas.paste(p, (x, y), p)
canvas.save(OUT / "pop-drop-themes.png", optimize=True)
print("background", BG)

# The gallery slide in the Event Sitters project drawer (src/assets/work/event-sitters-gallery.png,
# 2880x1800): the photos from the scrolling gallery on eventsitters.nz, in the site's own frames
# (a soft blob, rounded rectangles, circles) and sizes, laid out in two staggered rows on white
# that run off the edges, as the gallery does.
# Sources: "03_Working files/event-sitters-gallery/" (the site's /images/, 2026-11-22). Frame
# sizes and nudges are the site's (.gallery-marquee-item, in CSS px), scaled up.
# Usage: python3 scripts/cases/event-sitters-gallery.py   (from rco-website/, needs Pillow)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT.parent / "03_Working files/event-sitters-gallery"
OUT = ROOT / "src/assets/work/event-sitters-gallery.png"
W, H, BG = 2880, 1800, (255, 255, 255)
SCALE, GAP = 3.1, 26  # CSS px to slide px; gap between frames in CSS px
SS = 3  # masks drawn at 3x for smooth edges

# The site's soft blob (its mask SVG, in a 0-1 box), as points along the curve.
BLOB = "0.975 0.5C0.977 0.573 0.98 0.649 0.958 0.72C0.936 0.792 0.902 0.891 0.843 0.931C0.785 0.971 0.68 0.954 0.605 0.96C0.53 0.966 0.467 0.973 0.394 0.966C0.32 0.959 0.219 0.963 0.165 0.92C0.111 0.876 0.092 0.777 0.071 0.707C0.049 0.637 0.04 0.571 0.035 0.5C0.03 0.429 0.021 0.351 0.041 0.279C0.061 0.206 0.095 0.109 0.154 0.066C0.212 0.022 0.315 0.022 0.39 0.019C0.465 0.016 0.532 0.035 0.603 0.048C0.674 0.062 0.76 0.062 0.818 0.102C0.875 0.141 0.921 0.218 0.948 0.284C0.974 0.351 0.973 0.427 0.975 0.5"

# (photo, frame, width, height, nudge) in CSS px, in the site's order; two rows of four.
ROWS = [
    [("arts-crafts-santa", "soft", 224, 168, 0), ("toys-blocks-pyramid", "rounded", 176, 235, 0),
     ("arts-crafts-christmas-tree", "circle", 192, 192, 15), ("public-event-santa-crafts", "rounded", 224, 299, -18)],
    [("toys-blocks-building", "soft", 224, 168, 0), ("cozy-corner-tent", "soft", 176, 235, 0),
     ("event-sitter-with-child", "rounded", 192, 144, 12), ("public-event-christmas-market", "circle", 224, 224, -13)],
]
ROW_CENTRES = (470, 1350)
ROW_STARTS = (-260, 120)  # the second row shifted right, so the rows stagger


def blob_points(w, h, steps=24):
    nums = [float(n) for n in BLOB.replace("C", " ").split()]
    pts, (x0, y0) = [], (nums[0], nums[1])
    for i in range(2, len(nums), 6):
        x1, y1, x2, y2, x3, y3 = nums[i:i + 6]
        for s in range(steps):
            t = s / steps
            u = 1 - t
            pts.append(((u**3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t**3 * x3) * w,
                        (u**3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t**3 * y3) * h))
        x0, y0 = x3, y3
    return pts


def framed(name, frame, w, h):
    photo = ImageOps.fit(Image.open(SRC / f"{name}.jpg").convert("RGB"), (w, h), Image.LANCZOS)
    mask = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(mask)
    if frame == "circle":
        d.ellipse((0, 0, w * SS - 1, h * SS - 1), fill=255)
    elif frame == "rounded":
        d.rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), round(24 * SCALE * SS), fill=255)
    else:
        d.polygon(blob_points(w * SS, h * SS), fill=255)
    out = photo.convert("RGBA")
    out.putalpha(mask.resize((w, h), Image.LANCZOS))
    return out


canvas = Image.new("RGB", (W, H), BG)
shadow = Image.new("L", (W, H), 0)
placed = []
# Each row repeats the gallery from its own point until it runs off the right edge, as the
# marquee loops on the site.
ITEMS = ROWS[0] + ROWS[1]
for r, (centre, start) in enumerate(zip(ROW_CENTRES, ROW_STARTS)):
    x, k = start, r * 4
    while x < W:
        name, frame, cw, ch, nudge = ITEMS[k % len(ITEMS)]
        k += 1
        w, h = round(cw * SCALE), round(ch * SCALE)
        img = framed(name, frame, w, h)
        y = round(centre - h / 2 + nudge * SCALE)
        shadow.paste(img.getchannel("A").point(lambda v: v * 0.18), (x, y + 24), img.getchannel("A"))
        placed.append((img, x, y))
        x += w + round(GAP * SCALE)
canvas.paste((0, 0, 0), (0, 0), shadow.filter(ImageFilter.GaussianBlur(40)))
for img, x, y in placed:
    canvas.paste(img, (x, y), img)
canvas.save(OUT, optimize=True)
print(OUT, [(x, y, img.size) for img, x, y in placed])

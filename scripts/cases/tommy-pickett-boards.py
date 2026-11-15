# Tommy Pickett case images, drawn from the project's own files.
# - hero (16:9) and card (1:1): the tommypickett.com hero motif, the TOMMY / PICKETT wordmark in
#   Clash Grotesk on olive with the copper cutout of Tommy in front.
# - stack-*: single posters and covers for the homepage hero stack.
# - venues: the 2026 set in one row, each poster turned and nudged slightly at random; the phone
#   version in two rows of three.
# - covers (Greener in Waihi isn't Robin's, so left out), posters (+ phone versions in two columns) and the 2026 venue set (one wide row), on
#   the warm grey of the other case boards with a soft shadow.
# Usage: python3 tommy-pickett-boards.py "<Tommy Pickett folder>" <out dir>
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

root, out = Path(sys.argv[1]), Path(sys.argv[2])
site = root / "Website/07_Website 3.0"
FONT = site / "02_Files/ClashGrotesk_Complete/Fonts/OTF/ClashGrotesk-Semibold.otf"
PHOTO = site / "02_Files/tommy-hero.png"
OLIVE, OLIVE_LIGHT = (0x76, 0x78, 0x5A), (0x9E, 0xA1, 0x79)
BG = (242, 241, 238)


def wordmark_hero(w, h, text_w, top, photo_h, name):
    canvas = Image.new("RGB", (w, h), OLIVE)
    d = ImageDraw.Draw(canvas)
    # Size the font so the wider line (PICKETT) is text_w wide, with 0.04em tracking.
    def line_w(s, f):
        return sum(f.getlength(c) for c in s) + f.size * 0.04 * (len(s) - 1)
    size = 400
    f = ImageFont.truetype(str(FONT), size)
    size = round(size * text_w / max(line_w("TOMMY", f), line_w("PICKETT", f)))
    f = ImageFont.truetype(str(FONT), size)
    cap = f.getbbox("T")[3] - f.getbbox("T")[1]
    y = top
    for s in ("TOMMY", "PICKETT"):
        x = (w - line_w(s, f)) / 2
        for c in s:
            d.text((x, y - f.getbbox("T")[1]), c, font=f, fill=OLIVE_LIGHT)
            x += f.getlength(c) + size * 0.04
        y += size * 0.78
    photo = Image.open(PHOTO).convert("RGBA").resize((photo_h, photo_h), Image.LANCZOS)
    canvas.paste(photo, ((w - photo_h) // 2, h - photo_h), photo)
    canvas.save(out / f"tommy-pickett-{name}.png", optimize=True)
    print(name, canvas.size, "font", size, "cap", cap)


def board(files, name, w=2880, cols=None, pad_x=240, pad_y=140, gap=80, shadow=True):
    cols = cols or len(files)
    ims = [Image.open(f).convert("RGB") for f in files]
    tw = (w - 2 * pad_x - gap * (cols - 1)) // cols
    ims = [im.resize((tw, round(im.height * tw / im.width)), Image.LANCZOS) for im in ims]
    th = max(im.height for im in ims)
    rows = (len(ims) + cols - 1) // cols
    canvas = Image.new("RGB", (w, rows * th + (rows - 1) * gap + 2 * pad_y), BG)
    sh = Image.new("L", canvas.size, 0)
    sd = ImageDraw.Draw(sh)
    spots = []
    for i, im in enumerate(ims):
        # a short last row is centred
        in_row = min(cols, len(ims) - (i // cols) * cols)
        x = (w - in_row * tw - (in_row - 1) * gap) // 2 + (i % cols) * (tw + gap)
        y = pad_y + (i // cols) * (th + gap) + (th - im.height) // 2
        spots.append((x, y))
        sd.rectangle((x, y + 18, x + tw, y + im.height + 18), fill=70)
    if shadow:
        canvas.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(34)))
    for im, (x, y) in zip(ims, spots):
        canvas.paste(im, (x, y))
    canvas.save(out / f"tommy-pickett-{name}.png", optimize=True)
    print(name, canvas.size)


def scatter_board(files, name, w=2880, pad_x=180, pad_y=200, gap=72, seed=7, cols=None, row_gap=None):
    """Rows of posters, each turned and nudged a little at random (fixed seed, so reruns match).
    One row unless `cols` is given (the phone version uses two rows of three)."""
    import random
    rnd = random.Random(seed)
    cols = cols or len(files)
    row_gap = gap if row_gap is None else row_gap
    ims = [Image.open(f).convert("RGBA") for f in files]
    tw = (w - 2 * pad_x - gap * (cols - 1)) // cols
    ims = [im.resize((tw, round(im.height * tw / im.width)), Image.LANCZOS) for im in ims]
    th = max(im.height for im in ims)
    rows = (len(ims) + cols - 1) // cols
    canvas = Image.new("RGB", (w, rows * th + (rows - 1) * row_gap + 2 * pad_y), BG)
    nudge_x, nudge_y = round(14 * tw / 360), round(45 * tw / 360)
    placed = []
    for i, im in enumerate(ims):
        angle = rnd.uniform(-3.5, 3.5)
        dx, dy = rnd.randint(-nudge_x, nudge_x), rnd.randint(-nudge_y, nudge_y)
        rot = im.rotate(angle, resample=Image.BICUBIC, expand=True)
        cx = pad_x + (i % cols) * (tw + gap) + tw // 2 + dx
        cy = pad_y + (i // cols) * (th + row_gap) + th // 2 + dy
        placed.append((rot, cx - rot.width // 2, cy - rot.height // 2))
    blur, drop = round(34 * tw / 360), round(18 * tw / 360)
    sh = Image.new("L", canvas.size, 0)
    for rot, x, y in placed:
        sh.paste(rot.getchannel("A").point(lambda v: 70 if v else 0), (x, y + drop), rot.getchannel("A"))
    canvas.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(blur)))
    for rot, x, y in placed:
        canvas.paste(rot, (x, y), rot)
    canvas.save(out / f"tommy-pickett-{name}.png", optimize=True)
    print(name, canvas.size)


def pdf_page(pdf, tmp, dpi=150):
    stem = Path(tmp) / Path(pdf).stem.replace(" ", "-")
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", "1", "-l", "1", "-singlefile", str(pdf), str(stem)], check=True)
    return f"{stem}.png"


out.mkdir(parents=True, exist_ok=True)
wordmark_hero(2880, 1620, 2400, 150, 1620, "hero")
wordmark_hero(2000, 2000, 1840, 150, 1840, "card")

covers = [root / p for p in (
    "Streetlights/06_Production/Streetlights.jpg",
    "Rivertown/06_Production/Tommy Pickett - Rivertown.jpg",
    "Dive Deep/Cover.png",
)]
board(covers, "covers", pad_x=300, pad_y=200, gap=110)
board(covers, "covers-phone", w=1560, cols=2, pad_x=100, pad_y=100, gap=60)

with tempfile.TemporaryDirectory() as tmp:
    posters = [
        root / "Tour Poster 2023/06_Production/00_Tour Poster/Images/Tommy Pickett Tour Poster.jpg",
        root / "Tour Poster 2024/06_Production/Tommy Pickett Tour 2024.jpg",
        pdf_page(root / "Tour Poster 2025/06_Production/Tour Poster 2025 - Ross Pub - A4.pdf", tmp),
        root / "Tour Poster 2026/06_Production/October 2026/Tommy Pickett – Ross Pub.jpg",
    ]
    # Extra cards for the homepage hero stack (projects.ts `stack`): the last two poster styles
    # and the first and last cover, each on its own at 1800px on the long side.
    for src, nm in ((posters[2], "stack-poster-2025"), (posters[3], "stack-poster-2026")):
        im = Image.open(src).convert("RGB")
        im.resize((round(im.width * 1800 / im.height), 1800), Image.LANCZOS).save(out / f"tommy-pickett-{nm}.png", optimize=True)
    for src, nm in ((covers[0], "stack-cover-streetlights"), (covers[2], "stack-cover-dive-deep")):
        Image.open(src).convert("RGB").resize((1800, 1800), Image.LANCZOS).save(out / f"tommy-pickett-{nm}.png", optimize=True)
    board(posters, "posters")
    board(posters, "posters-phone", w=1560, cols=2, pad_x=100, pad_y=100, gap=60)

venues = [root / f"Tour Poster 2026/06_Production/October 2026/Tommy Pickett – {v}.jpg" for v in (
    "Sprig and Fern", "Golden Bear", "Railway Hotel", "Monsoon", "Cook Saddle", "Tuatara",
)]
scatter_board(venues, "venues")
scatter_board(venues, "venues-phone", w=1170, pad_x=90, pad_y=90, gap=56, cols=3, row_gap=90)

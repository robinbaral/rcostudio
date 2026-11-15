# Tommy Pickett case images, drawn from the project's own files.
# - hero (16:9) and card (1:1): the tommypickett.com hero motif, the TOMMY / PICKETT wordmark in
#   Clash Grotesk on olive with the copper cutout of Tommy in front.
# - stack-*: single posters and covers for the homepage hero stack.
# The covers, posters and venue set on the case page are separate images now (CaseBoard),
# taken from the same files by board-items.py.
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


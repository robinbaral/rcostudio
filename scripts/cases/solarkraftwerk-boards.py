# Solarkraftwerk drawer gallery (src/assets/work/solarkraftwerk-*.png, 2880x1800), from the
# brand presentation and the print files in ~/Projects/Solarkraftwerk:
# - logo-sketches: the eight logo ideas from "Solarkraftwerk Ideen.pdf" page 5, redrawn as pencil
#   sketches on graph paper in the style of the ProLog logo sketches (SVG filters, rendered in the
#   headless Chrome from scripts/capture).
# - logo: page 6 as laid out in the PDF, without its label, on the brand yellow.
# - cards-landscape, cards-portrait: the business card drafts of pages 14 and 15 where the PDF
#   places them, as separate cards with a soft shadow on the brand's dark slate, like the
#   Tommy Pickett boards.
# All fill the frame edge to edge in the drawer (galleryBleed in projects.ts).
# - print: the roof banner and both sides of the flyer on the warm grey of the other boards.
# Usage: python3 scripts/cases/solarkraftwerk-boards.py <work dir>   (from rco-website/)
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

Image.MAX_IMAGE_PIXELS = None
SRC = Path.home() / "Projects/Solarkraftwerk"
IDEEN = SRC / "01_Corporate Design/05_Outbox/Solarkraftwerk Ideen.pdf"
BANNER = SRC / "02_Banner/06_Production/Solarkraftwerk Banner Solardach.pdf"
# The banner as Robin exported it (2026-11-15), a little wider than the PDF's page; kept in
# 03_Working files and used instead of rendering the PDF.
BANNER_JPG = Path(__file__).resolve().parents[3] / "03_Working files/solarkraftwerk-banner-solardach.jpg"
FLYER = SRC / "04_Flyer/06_Production/Solarkraftwerk Flyer.pdf"
OUT = Path(__file__).resolve().parents[2] / "src/assets/work"
CHROME = Path.home() / "Library/Caches/ms-playwright/chromium_headless_shell-1148/chrome-mac/headless_shell"
W, H, BG = 2880, 1800, (242, 241, 238)
YELLOW, SLATE = (248, 235, 93), (44, 46, 51)  # the brand yellow and the dark grey of its type
tmp = Path(sys.argv[1]); tmp.mkdir(parents=True, exist_ok=True)


def render(pdf, dpi, stem, page=None):
    args = ["pdftoppm", "-r", str(dpi), "-png"] + (["-f", str(page), "-l", str(page), "-singlefile"] if page else [])
    subprocess.run(args + [str(pdf), str(tmp / stem)], check=True)


def runs(mask, gap):
    out, s, last = [], None, None
    for i, v in enumerate(mask):
        if v:
            if s is None: s = i
            elif i - last > gap: out.append((s, last + 1)); s = i
            last = i
    if s is not None: out.append((s, last + 1))
    return out


def sketches():
    render(IDEEN, 216, "ideen-5", 5)
    im = Image.open(tmp / "ideen-5.png").convert("L")
    sm = im.resize((im.width // 8, im.height // 8)); sp = sm.load(); w, h = sm.size; top = 1300 // 8
    icons = []
    rows = [(a + top, b + top) for a, b in runs([any(sp[x, y] < 128 for x in range(w)) for y in range(top, h)], 20)]
    for y0, y1 in rows:
        for x0, x1 in runs([any(sp[x, y] < 128 for y in range(y0, y1)) for x in range(w)], 20):
            c = im.crop((x0 * 8 - 32, y0 * 8 - 32, x1 * 8 + 32, y1 * 8 + 32))
            icon = Image.new("RGBA", c.size, (0, 0, 0, 0)); icon.putalpha(ImageOps.invert(c))
            r = 1150 / max(icon.size)
            f = tmp / f"icon-{len(icons)}.png"
            icon.resize((round(icon.width * r), round(icon.height * r)), Image.LANCZOS).save(f)
            icons.append(f)
    K = 0.55  # icons show about twice as large as ProLog's, so the pencil detail is scaled to match
    cells = []
    for n, f in enumerate(icons):
        w, h = Image.open(f).size
        cells.append(f'''<div class="cell"><svg viewBox="0 0 {w} {h}" style="height:{h / 1150 * 100:.0f}%"><defs>
 <filter id="o{n}" x="-10%" y="-10%" width="120%" height="120%">
  <feMorphology in="SourceAlpha" operator="dilate" radius="7" result="d"/>
  <feComposite in="d" in2="SourceAlpha" operator="out" result="ring"/>
  <feTurbulence type="fractalNoise" baseFrequency="{0.018 / K:.4f}" numOctaves="2" seed="{n * 3 + 1}" result="t"/>
  <feDisplacementMap in="ring" in2="t" scale="{20 * K:.1f}" xChannelSelector="R" yChannelSelector="G" result="a"/>
  <feTurbulence type="fractalNoise" baseFrequency="{0.03 / K:.4f}" numOctaves="2" seed="{n * 3 + 2}" result="t2"/>
  <feDisplacementMap in="ring" in2="t2" scale="{30 * K:.1f}" xChannelSelector="G" yChannelSelector="R" result="b"/>
  <feTurbulence type="fractalNoise" baseFrequency="{0.9 / K:.3f}" numOctaves="1" seed="{n}" result="grain"/>
  <feColorMatrix in="grain" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -0.9 1.35" result="g"/>
  <feMerge result="m"><feMergeNode in="a"/><feMergeNode in="b"/></feMerge>
  <feComposite in="m" in2="g" operator="in" result="lines"/>
  <feFlood flood-color="#1c1c1c"/><feComposite in2="lines" operator="in"/>
 </filter>
 <filter id="h{n}" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="{0.005 / K:.4f}" numOctaves="2" seed="{n * 5}" result="t"/>
  <feDisplacementMap in="SourceGraphic" in2="t" scale="{12 * K:.1f}" xChannelSelector="R" yChannelSelector="G"/>
 </filter>
 <pattern id="p{n}" width="{24 * K:.1f}" height="{24 * K:.1f}" patternUnits="userSpaceOnUse" patternTransform="rotate({35 + n * 7 % 30})">
  <line x1="0" y1="0" x2="0" y2="{24 * K:.1f}" stroke="#1c1c1c" stroke-width="3.4" opacity=".62"/>
 </pattern>
 <mask id="m{n}"><image href="{f}" width="{w}" height="{h}" style="filter:brightness(0) invert(1)"/></mask>
</defs>
<g filter="url(#h{n})"><rect width="4000" height="4000" fill="url(#p{n})" mask="url(#m{n})"/></g>
<image href="{f}" width="{w}" height="{h}" filter="url(#o{n})"/></svg></div>''')
    html = tmp / "sketch.html"
    html.write_text(f'''<!doctype html><meta charset=utf-8><style>
html,body{{margin:0;background:#f3f1ec}}
.sheet{{width:1440px;height:900px;padding:0 150px;box-sizing:border-box;display:grid;grid-template-columns:repeat(4,1fr);gap:110px 120px;align-content:center;
 background-image:linear-gradient(#e4e1d9 1px,transparent 1px),linear-gradient(90deg,#e4e1d9 1px,transparent 1px);background-size:40px 40px;background-position:-1px -1px}}
.cell{{height:230px;display:flex;align-items:center;justify-content:center}}
.cell svg{{max-width:100%;overflow:visible}}
</style><div class="sheet">{"".join(cells)}</div>''')
    subprocess.run([str(CHROME), "--headless", "--hide-scrollbars", "--force-device-scale-factor=2", "--window-size=1440,900",
                    "--allow-file-access-from-files", f"--screenshot={OUT / 'solarkraftwerk-logo-sketches.png'}", f"file://{html}"],
                   check=True, capture_output=True)


def load_page(n):
    render(IDEEN, 216, f"ideen-{n}", n)
    im = Image.open(tmp / f"ideen-{n}.png").convert("RGB")
    ImageDraw.Draw(im).rectangle((0, 0, im.width, int(im.height * 0.18)), fill="white")  # page label
    return im


def logo_page():
    """Page 6 as laid out, on the brand yellow (multiplied, so black stays black)."""
    im = load_page(6)
    box = ImageChops.difference(im, Image.new("RGB", im.size, "white")).convert("L").point(lambda v: 255 if v > 6 else 0).getbbox()
    c = im.crop(box)
    s = min((W - 600) / c.width, (H - 500) / c.height)
    c = c.resize((round(c.width * s), round(c.height * s)), Image.LANCZOS)
    out = Image.new("RGB", (W, H), "white"); out.paste(c, ((W - c.width) // 2, (H - c.height) // 2))
    ImageChops.multiply(out, Image.new("RGB", (W, H), YELLOW)).save(OUT / "solarkraftwerk-logo.png")


def cards(n, name, pad):
    """The business cards of a page, kept where the PDF places them, as separate cards with a soft
    shadow, like the Tommy Pickett poster and cover boards; on the brand's dark slate, so the
    light grey and yellow cards stand out."""
    im = load_page(n)
    ink = ImageChops.difference(im, Image.new("RGB", im.size, "white")).convert("L").point(lambda v: 255 if v > 3 else 0)
    sm = ink.resize((im.width // 8, im.height // 8)); sp = sm.load(); w, h = sm.size
    boxes = []
    for y0, y1 in runs([any(sp[x, y] for x in range(w)) for y in range(h)], 4):
        for x0, x1 in runs([any(sp[x, y] for y in range(y0, y1)) for x in range(w)], 4):
            b = ink.crop((x0 * 8 - 8, y0 * 8 - 8, x1 * 8 + 8, y1 * 8 + 8)).getbbox()
            boxes.append((x0 * 8 - 8 + b[0], y0 * 8 - 8 + b[1], x0 * 8 - 8 + b[2], y0 * 8 - 8 + b[3]))
    X0, Y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    X1, Y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    s = min((W - 2 * pad) / (X1 - X0), (H - 2 * pad) / (Y1 - Y0))
    ox, oy = (W - (X1 - X0) * s) / 2, (H - (Y1 - Y0) * s) / 2
    spots = []
    for b in boxes:
        c = im.crop(b); c = c.resize((round(c.width * s), round(c.height * s)), Image.LANCZOS)
        spots.append((c, round(ox + (b[0] - X0) * s), round(oy + (b[1] - Y0) * s)))
    canvas = Image.new("RGB", (W, H), SLATE); sh = Image.new("L", (W, H), 0); d = ImageDraw.Draw(sh)
    for c, x, y in spots: d.rectangle((x, y + 16, x + c.width, y + c.height + 16), fill=120)
    canvas.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(28)))
    for c, x, y in spots: canvas.paste(c, (x, y))
    canvas.save(OUT / f"solarkraftwerk-{name}.png")
    return len(boxes)


def print_board():
    render(FLYER, 300, "flyer")
    gap = 56
    b = Image.open(BANNER_JPG).convert("RGB")
    fl = [Image.open(tmp / f"flyer-{i}.png").convert("RGB") for i in (1, 2)]
    # The height that leaves the same margin at the sides as above and below.
    width = lambda bh: b.width * bh / b.height + gap * 1.6 + fl[0].width * ((bh - gap) / 2) / fl[0].height
    bh = max(range(600, H), key=lambda h: h if W - width(h) >= H - h else 0)
    pad_y = (H - bh) // 2
    b = b.resize((round(b.width * bh / b.height), bh), Image.LANCZOS)
    fh = (bh - gap) // 2
    fl = [f.resize((round(f.width * fh / f.height), fh), Image.LANCZOS) for f in fl]
    x0 = round((W - b.width - gap * 1.6 - fl[0].width) / 2); xf = round(x0 + b.width + gap * 1.6)
    spots = [(b, x0, pad_y), (fl[0], xf, pad_y), (fl[1], xf, pad_y + fh + gap)]
    canvas = Image.new("RGB", (W, H), BG); sh = Image.new("L", (W, H), 0); d = ImageDraw.Draw(sh)
    for im, x, y in spots: d.rectangle((x, y + 18, x + im.width, y + im.height + 18), fill=60)
    canvas.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(30)))
    for im, x, y in spots: canvas.paste(im, (x, y))
    canvas.save(OUT / "solarkraftwerk-print.png")


if "--skip-sketches" not in sys.argv: sketches()
logo_page()
print("landscape cards", cards(14, "cards-landscape", 200))
print("portrait cards", cards(15, "cards-portrait", 200))
print_board()

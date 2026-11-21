# Still images of Tommy Pickett's covers and posters boards (src/assets/work/
# tommy-pickett-covers.png, tommy-pickett-posters.png, 2880x1800), for the hover preview and its
# thumbnails. The drawer itself shows the live boards (CaseBoard, settings in
# src/data/projects.ts); these follow its 16:10 layout: one row on the light board colour, the
# side padding (% of the width), the pieces overlapping by the negative gap, each turned and
# nudged by CaseBoard's own seeded values (tilt), with the same box shadow.
# Usage: python3 scripts/cases/tommy-pickett-board-stills.py   (from rco-website/, needs Pillow)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
BOARDS = ROOT / "src/assets/cases/tommy-pickett/boards"
OUT = ROOT / "src/assets/work"
W, H, BG = 2880, 1800, (242, 241, 238)  # --board, light mode (global.css)
SS = 2  # drawn at 2x, then scaled down for smooth edges


def turns(n):
    """CaseBoard's turns: rotation (deg) and nudge (% of the piece's height) per piece."""
    seed, out = 7, []
    for _ in range(n):
        seed = seed * 16807 % 2147483647
        r = seed / 2147483647 * 7 - 3.5
        seed = seed * 16807 % 2147483647
        y = seed / 2147483647 * 10 - 5
        out.append((r, y))
    return out


def still(name, pad, gap):
    pieces = [Image.open(p).convert("RGB") for p in sorted((BOARDS / f"tommy-pickett-{name}").glob("*.jpg"))]
    w, h = W * SS, H * SS
    n = len(pieces)
    inner = w * (1 - 2 * pad / 100)
    ratios = [p.width / p.height for p in pieces]
    # Widths share the inner width plus the overlaps, so the row fills it (CaseBoard).
    widths = [(inner - (n - 1) * w * gap / 100) * r / sum(ratios) for r in ratios]
    canvas = Image.new("RGB", (w, h), BG)
    x = w * pad / 100
    for p, pw, (rot, nudge) in zip(pieces, widths, turns(n)):
        ph = pw / (p.width / p.height)
        img = p.resize((round(pw), round(ph)), Image.LANCZOS).convert("RGBA")
        cx, cy = x + pw / 2, h / 2 + ph * nudge / 100
        # Box shadow: 0 1.2cqw 3cqw rgb(0 0 0 / 0.22), turned with the piece.
        m = round(w * 0.06)
        sh = Image.new("L", (img.width + 2 * m, img.height + 2 * m), 0)
        ImageDraw.Draw(sh).rectangle((m, m, m + img.width, m + img.height), fill=56)
        sh = sh.filter(ImageFilter.GaussianBlur(w * 0.015)).rotate(rot * -1, resample=Image.BICUBIC, expand=True)
        canvas.paste((0, 0, 0), (round(cx - sh.width / 2), round(cy + w * 0.012 - sh.height / 2)), sh)
        turned = img.rotate(rot * -1, resample=Image.BICUBIC, expand=True)
        canvas.paste(turned, (round(cx - turned.width / 2), round(cy - turned.height / 2)), turned)
        x += pw + w * gap / 100
    canvas.resize((W, H), Image.LANCZOS).save(OUT / f"tommy-pickett-{name}.png", optimize=True)
    print(name, "piece widths", [round(v / SS) for v in widths])


# Padding and gap as in the drawer (galleryBoard in src/data/projects.ts).
still("covers", 7, -3)
still("posters", 6, -2.5)

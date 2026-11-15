# Phone versions of the wide case boards (rows of screens, icons or posters). Finds each element
# on the flat board background, keeps a selection of them and lays them out again in fewer
# columns, so phones show a smaller set at a readable size instead of a strip to scroll.
# Writes <name>-phone.png next to each source. (Tommy Pickett's turned posters get theirs from
# tommy-pickett-boards.py, which can redraw the soft shadows.)
# Usage: python3 scripts/cases/case-phone-boards.py   (from rco-website/)
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2] / "src/assets/cases"
W = 1170          # 3x a 390px phone column
PAD, GAP = 64, 28


def runs(mask, min_gap=10, min_len=20):
    """Index ranges where mask is true, joining gaps shorter than min_gap."""
    out, start, last = [], None, None
    for i, on in enumerate(mask):
        if on:
            if start is None:
                start = i
            elif i - last > min_gap:
                out.append((start, last + 1))
                start = i
            last = i
    if start is not None:
        out.append((start, last + 1))
    return [r for r in out if r[1] - r[0] >= min_len]


def elements(im, tol=14):
    """Element boxes in reading order (rows, then left to right)."""
    bg = im.getpixel((3, 3))
    px = im.load()
    w, h = im.size
    step = 2

    def fg(x, y):
        p = px[x, y]
        return max(abs(p[i] - bg[i]) for i in range(3)) > tol

    rows = runs([any(fg(x, y) for x in range(0, w, 6)) for y in range(h)], min_gap=24)
    boxes = []
    for y0, y1 in rows:
        cols = runs([any(fg(x, y) for y in range(y0, y1, step)) for x in range(w)], min_gap=12)
        for x0, x1 in cols:
            ys = runs([any(fg(x, y) for x in range(x0, x1, step)) for y in range(y0, y1)], min_gap=24)
            boxes.append((x0, y0 + ys[0][0], x1, y0 + ys[-1][1]))
    return bg, boxes


def compose(src, layout, out, tol=14, to_scale=False, shadow=False, crop_ratio=None):
    """`to_scale` keeps one scale for every element (devices shown at their real sizes) and
    bottom-aligns each row; otherwise each row is scaled to fill the width at one height."""
    im = Image.open(src).convert("RGB")
    bg, boxes = elements(im, tol)
    crops = [im.crop(b) for b in boxes]
    if crop_ratio:
        # Tall pages: keep the top, crop_ratio x the width, and let it bleed off the bottom
        # of the board as the desktop version does.
        crops = [c.crop((0, 0, c.width, min(c.height, round(c.width * crop_ratio)))) for c in crops]
    rows = [[crops[i] for i in row] for row in layout]
    inner = W - 2 * PAD
    fit = [(inner - GAP * (len(r) - 1)) / sum(c.width for c in r) for r in rows]
    scaled = []
    for row, f in zip(rows, fit):
        if to_scale:
            f = min(fit)
        else:
            hh = (inner - GAP * (len(row) - 1)) / sum(c.width / c.height for c in row)
            f = [hh / c.height for c in row]
        fs = f if isinstance(f, list) else [f] * len(row)
        scaled.append([c.resize((round(c.width * k), round(c.height * k)), Image.LANCZOS) for c, k in zip(row, fs)])
    heights = [max(c.height for c in r) for r in scaled]
    H = (PAD if crop_ratio else 2 * PAD) + sum(heights) + GAP * (len(scaled) - 1)
    canvas = Image.new("RGB", (W, round(H)), bg)
    y = PAD
    spots = []
    for row, rh in zip(scaled, heights):
        rw = sum(c.width for c in row) + GAP * (len(row) - 1)
        x = (W - rw) // 2
        for c in row:
            # Only the element itself, not the board's background (or its old shadow) in the
            # corners of the crop.
            diff = ImageChops.difference(c, Image.new("RGB", c.size, bg)).convert("L")
            edge = diff.point(lambda v: 255 if v > 30 else 0).filter(ImageFilter.MaxFilter(3))
            # Solid inside the outline: flood the outside from the corners, keep the rest.
            outside = Image.new("L", (c.width + 2, c.height + 2), 0)
            outside.paste(edge, (1, 1))
            ImageDraw.floodfill(outside, (0, 0), 128)
            mask = outside.crop((1, 1, c.width + 1, c.height + 1)).point(lambda v: 0 if v == 128 else 255)
            spots.append((c, mask, x, y + rh - c.height))
            x += c.width + GAP
        y += rh + GAP
    if shadow:
        # A soft drop shadow drawn again at the new size, like the one on the desktop board.
        sh = Image.new("L", canvas.size, 0)
        for c, mask, x, yy in spots:
            sh.paste(mask.point(lambda v: 60 if v else 0), (x, yy + 12), mask)
        canvas.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(22)))
    for c, mask, x, yy in spots:
        canvas.paste(c, (x, yy), mask if shadow else None)
    canvas.save(out)
    return len(boxes), canvas.size


cc = ROOT / "crisscross"
jobs = {
    # name: rows of element indices (reading order of the desktop board)
    "crisscross-puzzle-screens": [[0, 3, 5]],
    "crisscross-theme-range": [[0, 1, 5]],
    "crisscross-app-icons-rounded": [[0, 1, 2, 3], [8, 9, 10, 11], [4, 5, 6, 7]],
    "crisscross-medal-editor-v4": [[0, 1, 4]],
    "crisscross-badges": [[0, 1, 2, 3], [4, 5, 6, 7], [11, 12, 13, 14]],
    "crisscross-paywalls": [[0, 2, 4]],
    "crisscross-home-cards": [[0, 1, 2], [3]],
}
if __name__ == "__main__":
    for name, layout in jobs.items():
        n, size = compose(cc / f"{name}.png", layout, cc / f"{name}-phone.png")
        print(name, n, "elements ->", size)
    # Devices to scale: phones in the first row, the iPad and the open Duo (one group on the board) in the second.
    n, size = compose(cc / "crisscross-device-lineup.png", [[0, 1], [2]],
                      cc / "crisscross-device-lineup-phone.png", tol=30, to_scale=True, shadow=True)
    print("crisscross-device-lineup", n, "elements ->", size)
    # ProLog: two of the three page concepts (article and audit page), larger, cropped to the top.
    pl = ROOT / "prolog"
    n, size = compose(pl / "prolog-page-concepts.png", [[0, 2]], pl / "prolog-page-concepts-phone.png", crop_ratio=1.5)
    print("prolog-page-concepts", n, "elements ->", size)

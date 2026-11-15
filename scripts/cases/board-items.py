# The pieces of the case boards as separate images, for CaseBoard (src/components/cases/), which
# lays them out on a CSS background: light or dark with the page, fewer per row on phones.
# Writes src/assets/cases/<case>/boards/<board>/<board>-NN.png (or .jpg for photos).
#
# - Boards exported flat (CrissCross screens, icons, badges; ProLog slides and pages): each
#   element is cut from the board image. The outside is every pixel that reads as the board
#   colour, shadowed or not (the colour times k, with no sharp step between neighbours),
#   reached from the edge of the element's box. Old baked-in shadows go with it; CSS draws
#   its own. Pixels along the edge are part element, part board: they get partial alpha and
#   their element colour back, so there's no light fringe on a dark background. A last pass
#   (defringe) catches board colour still left solid along dark outlines.
# - Tommy Pickett's covers and posters come straight from the project files (no shadow to
#   remove), as JPGs.
# Pencil sketches on graph paper stay single images (paper is the medium there).
# Usage: python3 scripts/cases/board-items.py [board ...]   (from rco-website/; default: all)
import subprocess, sys, tempfile, warnings
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "src/assets/cases"
TOMMY = Path.home() / "Projects/Tommy Pickett"


# Finding the elements on a board: runs of non-board pixels, rows first, then columns.
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




def out_ring(out):
    """Pixels within 24px of the outside: specks are only cleared there, never deep inside."""
    return np.asarray(Image.fromarray((out * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(49))) > 0


def cut(rgb, B, blur=0.0):
    """One element (RGB array, with some board around it) -> RGBA array, cropped to it."""
    h, w, _ = rgb.shape
    # Detected on a lightly smoothed copy: dithered shadows would otherwise read as edges.
    soft = np.asarray(Image.fromarray(rgb.astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))).astype(float) if blur else rgb
    lum = soft @ [0.299, 0.587, 0.114]
    k = lum / (B @ [0.299, 0.587, 0.114])
    like = np.abs(soft - k[..., None] * B).max(2) < 7
    step = np.zeros_like(lum)
    step[:, 1:] = np.maximum(step[:, 1:], np.abs(np.diff(lum, axis=1)))
    step[:, :-1] = np.maximum(step[:, :-1], np.abs(np.diff(lum, axis=1)))
    step[1:, :] = np.maximum(step[1:, :], np.abs(np.diff(lum, axis=0)))
    step[:-1, :] = np.maximum(step[:-1, :], np.abs(np.diff(lum, axis=0)))
    cand = like & (k > 0.3) & (k < 1.02) & (step < 3)
    m = Image.fromarray((cand * 255).astype(np.uint8)).copy()  # writable, or floodfill does nothing
    for x in range(0, w, 3):
        for y in (0, h - 1):
            if m.getpixel((x, y)) == 255: ImageDraw.floodfill(m, (x, y), 128)
    for y in range(0, h, 3):
        for x in (0, w - 1):
            if m.getpixel((x, y)) == 255: ImageDraw.floodfill(m, (x, y), 128)
    out = np.asarray(m) == 128
    # Specks left in the shadow (a few pixels that missed the fill) go with the outside.
    keep = Image.fromarray(((~out) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5))
    out = out | ((np.asarray(keep) == 0) & ~np.asarray(Image.fromarray(((~out) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3))).astype(bool) & out_ring(out))
    # Only the element at the centre of the box: bits of a neighbour caught in the margin go.
    body = Image.fromarray(((~out) * 255).astype(np.uint8)).copy()
    cy, cx = h // 2, w // 2
    xs = [x for x in sorted(range(w), key=lambda x: abs(x - cx)) if body.getpixel((x, cy)) == 255]
    if xs:
        ImageDraw.floodfill(body, (xs[0], cy), 128)
        out = np.asarray(body) != 128
    lum = rgb @ [0.299, 0.587, 0.114]
    k = lum / (B @ [0.299, 0.587, 0.114])
    # Edge band (2px into the element): the share of board colour in each pixel, from how
    # close it is to the local board shade, relative to the element colour just inside.
    near = np.asarray(Image.fromarray((out * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
    band = near & ~out
    kk = np.where(out, k, np.nan)
    kk_local = np.asarray(Image.fromarray(np.nan_to_num(kk * 100).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))).astype(float) / 100
    Bk = np.clip(kk_local, 0.3, 1.02)[..., None] * B
    inner = ~near
    # element colour: nearest inner pixel, approximated by a max-difference pick in a 7x7 window
    d = np.abs(rgb - Bk).max(2)
    dmax = np.asarray(Image.fromarray(np.clip(np.where(inner, d, 0), 0, 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))).astype(float)
    alpha = np.where(out, 0.0, 1.0)
    a = np.clip(d / np.maximum(dmax, 1), 0, 1)
    alpha[band] = a[band]
    colour = rgb.copy()
    safe = np.maximum(alpha, 1e-3)[..., None]
    colour[band] = np.clip((rgb[band] - (1 - alpha[band])[:, None] * Bk[band]) / safe[band], 0, 255)
    colour, alpha = defringe(colour, alpha, B)
    rgba = np.dstack([colour, alpha * 255]).round().astype(np.uint8)
    ys, xs = np.where(alpha > 0.02)
    return rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def defringe(colour, alpha, B, ring=3):
    """Board colour left along the outline, mostly beside dark edges (phone frames, icon
    outlines), where the cut keeps a pixel or two of light board as solid: a jagged light rim
    on a dark board. Each pixel within `ring` px of the outside is seen as it was on the board,
    then split again into the element colour just inside it (spread outwards from the solid
    core) and board, which sets its alpha. Only where that element colour is dark: light
    elements (white screens, pastel themes) are cut cleanly already."""
    out = alpha < 0.02
    grow = lambda m, r: np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * r + 1))) > 0
    band = grow(out, ring) & ~out
    seen = alpha[..., None] * colour + (1 - alpha[..., None]) * B  # as on the board
    # Element colour for the band: the solid core's colours, spread out a pixel at a time.
    inner = np.where(band[..., None], np.nan, colour.astype(float))
    inner[out] = np.nan
    for _ in range(ring + 2):
        todo = np.isnan(inner[..., 0]) & band
        if not todo.any():
            break
        pad = np.pad(inner, ((1, 1), (1, 1), (0, 0)), constant_values=np.nan)
        stack = np.stack([pad[1 + dy:pad.shape[0] - 1 + dy, 1 + dx:pad.shape[1] - 1 + dx]
                          for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx])
        with np.errstate(invalid="ignore"), warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)  # all-empty neighbourhoods
            mean = np.nanmean(stack, axis=0)
        inner[todo] = mean[todo]
    I = inner
    diff = I - B
    span = (diff ** 2).sum(2)
    # Only beside dark element colours, where a light rim shows; light elements were cut
    # cleanly already, and splitting their faint edge against the board adds a grey line.
    dark = (np.nan_to_num(I, nan=255.0) @ [0.299, 0.587, 0.114]) < 110
    ok = band & ~np.isnan(span) & (span > 40 ** 2) & dark
    with np.errstate(invalid="ignore", divide="ignore"):
        a = np.clip(((seen - B) * diff).sum(2) / span, 0, 1)
    alpha = alpha.copy()
    colour = colour.copy()
    alpha[ok] = a[ok]
    colour[ok] = I[ok]
    return colour, alpha


def from_board(case, board, tol=14, margin=40, blur=0.0):
    src = CASES / case / f"{board}.png"
    im = Image.open(src).convert("RGB")
    _, boxes = elements(im, tol)
    a = np.asarray(im).astype(float)
    B = np.median(np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3), a[:, :4].reshape(-1, 3)]), axis=0)
    out_dir = CASES / case / "boards" / board
    out_dir.mkdir(parents=True, exist_ok=True)
    for f in out_dir.glob("*"):
        f.unlink()
    H, W = a.shape[:2]
    for i, (x0, y0, x1, y1) in enumerate(boxes, 1):
        x0, y0 = max(0, x0 - margin), max(0, y0 - margin)
        x1, y1 = min(W, x1 + margin), min(H, y1 + margin)
        if board in RATIO:
            # Plain rectangles of a known shape: the box's width from its top-left corner (the
            # shadow only falls below), at that ratio. No colour guessing needed.
            bx0, by0, bx1, _ = boxes[i - 1]
            piece = np.dstack([a[by0:by0 + round((bx1 - bx0) / RATIO[board]), bx0:bx1], np.full((round((bx1 - bx0) / RATIO[board]), bx1 - bx0), 255.0)]).astype(np.uint8)
        else:
            piece = cut(a[y0:y1, x0:x1], B, blur)
        Image.fromarray(piece).save(out_dir / f"{board}-{i:02d}.png", optimize=True)
    print(f"{case}/{board}: {len(boxes)} pieces")


def from_files(case, board, files, width=1100):
    out_dir = CASES / case / "boards" / board
    out_dir.mkdir(parents=True, exist_ok=True)
    for f in out_dir.glob("*"):
        f.unlink()
    for i, f in enumerate(files, 1):
        im = Image.open(f).convert("RGB")
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(out_dir / f"{board}-{i:02d}.jpg", quality=92)
    print(f"{case}/{board}: {len(files)} pieces")


def pdf_page(pdf, tmp, dpi=150):
    stem = Path(tmp) / Path(pdf).stem.replace(" ", "-")
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", "1", "-l", "1", "-singlefile", str(pdf), str(stem)], check=True)
    return f"{stem}.png"


FLAT = {
    "crisscross-puzzle-screens": "crisscross", "crisscross-theme-range": "crisscross",
    "crisscross-app-icons-rounded": "crisscross", "crisscross-medal-editor-v4": "crisscross",
    "crisscross-badges": "crisscross", "crisscross-paywalls": "crisscross",
    "crisscross-home-cards": "crisscross", "crisscross-device-lineup": "crisscross",
    "crisscross-puzzle-studio": "crisscross",
    "prolog-slides": "prolog", "prolog-page-concepts": "prolog",
}
TOL = {"crisscross-device-lineup": 30}
# Pieces this close together (the slides sit 36px apart) are cut with a tight margin, so no
# neighbour's edge gets into the cut.
MARGIN = {"prolog-slides": 6}
# Slides: 16:9 rectangles, cut by shape instead.
RATIO = {"prolog-slides": 16 / 9}
# Dithered shadows (the device line-up) are smoothed before the board is found, or their
# speckle reads as edges; elsewhere that would blur faint outlines away.
BLUR = {"crisscross-device-lineup": 1.2}

want = set(sys.argv[1:])
for board, case in FLAT.items():
    if not want or board in want:
        from_board(case, board, TOL.get(board, 14), MARGIN.get(board, 40), BLUR.get(board, 0.0))

if not want or want & {"tommy-pickett-covers", "tommy-pickett-posters", "tommy-pickett-venues"}:
    covers = [TOMMY / p for p in ("Streetlights/06_Production/Streetlights.jpg",
                                  "Rivertown/06_Production/Tommy Pickett - Rivertown.jpg",
                                  "Dive Deep/Cover.png")]
    venues = [TOMMY / f"Tour Poster 2026/06_Production/October 2026/Tommy Pickett – {v}.jpg"
              for v in ("Sprig and Fern", "Golden Bear", "Railway Hotel", "Monsoon", "Cook Saddle", "Tuatara")]
    with tempfile.TemporaryDirectory() as tmp:
        posters = [TOMMY / "Tour Poster 2023/06_Production/00_Tour Poster/Images/Tommy Pickett Tour Poster.jpg",
                   TOMMY / "Tour Poster 2024/06_Production/Tommy Pickett Tour 2024.jpg",
                   pdf_page(TOMMY / "Tour Poster 2025/06_Production/Tour Poster 2025 - Ross Pub - A4.pdf", tmp),
                   TOMMY / "Tour Poster 2026/06_Production/October 2026/Tommy Pickett – Ross Pub.jpg"]
        from_files("tommy-pickett", "tommy-pickett-covers", covers)
        from_files("tommy-pickett", "tommy-pickett-posters", posters)
        from_files("tommy-pickett", "tommy-pickett-venues", venues, width=900)

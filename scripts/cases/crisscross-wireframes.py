# Turns the first three screens of the CrissCross puzzle-screen board into wireframes (grey
# tones, black lines, white screens with a thin outline), so the row reads from early
# structure to the finished, coloured screens. Reads the untouched colour board from
# "03_Working files/crisscross-puzzle-screens-colour.png" and writes
# src/assets/cases/crisscross/crisscross-puzzle-screens.png; run board-items.py after it to
# cut the screens apart for the case page. Screens listed in SWAPS are replaced first by a newer export from
# the CrissCross Figma file (also in "03_Working files/"), fitted into the old screen's shape.
# Usage: python3 scripts/cases/crisscross-wireframes.py   (from rco-website/)
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT.parent / "03_Working files/crisscross-puzzle-screens-colour.png"
OUT = ROOT / "src/assets/cases/crisscross/crisscross-puzzle-screens.png"
SWAPS = {3: "crisscross-puzzle-screen-1-2252.png"}   # index from the left: Figma node 1:2252
COUNT = 3                      # screens to turn into wireframes, from the left
OUTLINE = (223, 222, 219)      # the first screen's own outline colour
# Lightness relative to the screen's background -> grey: ink stays ink, tiles and filled
# cells become light greys, empty cells a faint grey, the background white.
T = [0.0, 0.25, 0.42, 0.85, 0.97, 1.0]
V = [28, 28, 214, 232, 247, 255]

im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(float)
bg = a[3, 3]
fg = np.abs(a - bg).max(2) > 12
cols = np.where(fg.any(0))[0]
boxes, s, p = [], cols[0], cols[0]
for c in cols[1:]:
    if c > p + 5:
        boxes.append((s, p + 1)); s = c
    p = c
boxes.append((s, p + 1))

def phone_mask(region):
    """The phone's whole shape: filled row by row, so pixels inside that happen to match the
    board background (antialiased corners) don't punch holes into it."""
    m = np.zeros_like(region)
    for i, row in enumerate(region):
        xs = np.where(row)[0]
        if len(xs):
            m[i, xs[0]:xs[-1] + 1] = True
    return m


for i, name in SWAPS.items():
    x0, x1 = boxes[i]
    rows = np.where(fg[:, x0:x1].any(1))[0]
    y0, y1 = rows.min(), rows.max() + 1
    m = phone_mask(fg[y0:y1, x0:x1])
    new = Image.open(SRC.parent / name).convert("RGB").resize((x1 - x0, y1 - y0), Image.LANCZOS)
    a[y0:y1, x0:x1][m] = np.asarray(new).astype(float)[m]
    fg[y0:y1, x0:x1] = m

out = a.copy()
lum = a @ [0.299, 0.587, 0.114]
for x0, x1 in boxes[:COUNT]:
    region = fg[:, x0:x1]
    rows = np.where(region.any(1))[0]
    y0, y1 = rows.min(), rows.max() + 1
    screen_l = np.median(lum[y0 + 40:y0 + 120, x0 + 60:x1 - 60])   # the screen's background
    L = lum[y0:y1, x0:x1]
    # Tones brighter than the screen (a white board with grey cells, as on the fourth screen)
    # are measured against white instead, so their cells stay visible.
    t = np.clip(np.where(L > screen_l + 4, L / 255, L / screen_l), 0, 1)
    grey = np.interp(t, T, V)
    m = phone_mask(region[y0:y1])
    block = out[y0:y1, x0:x1]
    for ch in range(3):
        block[..., ch] = np.where(m, grey, block[..., ch])
    # A thin outline around the phone, as on the first (white) screen.
    # (Padded first: the filter would otherwise treat the crop's border as more phone.)
    mask = Image.fromarray(np.pad(m, 4).astype(np.uint8) * 255)
    inner = np.asarray(mask.filter(ImageFilter.MinFilter(5))).astype(bool)[4:-4, 4:-4]
    edge = m & ~inner
    block[edge] = OUTLINE

Image.fromarray(out.astype(np.uint8)).save(OUT)
print("wireframed", COUNT, "of", len(boxes), "screens ->", OUT.name)

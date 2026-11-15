# python3 match.py <full.png> <old.webp> [<old.webp> ...]
# Finds the scroll offset of each old screenshot within a full-page capture (same CSS width).
# Prints name, best y, and the mean abs difference (0-255; under ~6 is a good match).
import sys
import numpy as np
from PIL import Image

full = Image.open(sys.argv[1]).convert("L")
F = 4
fw = full.width // F
fa = np.asarray(full.resize((fw, full.height // F), Image.BILINEAR), dtype=np.float32)
for p in sys.argv[2:]:
    old = Image.open(p).convert("L")
    # old shots are at 2x of the CSS size for mobile (780 wide for 390) or 1x for desktop (1440)
    css_w = full.width
    k = old.width / css_w
    css_h = round(old.height / k)
    o = np.asarray(old.resize((fw, css_h // F), Image.BILINEAR), dtype=np.float32)
    best = (1e9, 0)
    for y in range(0, fa.shape[0] - o.shape[0] + 1):
        d = np.abs(fa[y : y + o.shape[0]] - o).mean()
        if d < best[0]:
            best = (d, y)
    d, y = best
    # refine at full res around y*F
    fl = np.asarray(full, dtype=np.float32)
    ol = np.asarray(old.resize((full.width, css_h), Image.BILINEAR), dtype=np.float32)
    rb = (1e9, 0)
    for yy in range(max(0, y * F - F * 2), min(full.height - css_h, y * F + F * 2) + 1):
        dd = np.abs(fl[yy : yy + css_h] - ol).mean()
        if dd < rb[0]:
            rb = (dd, yy)
    print(p.rsplit("/", 1)[-1], rb[1], round(rb[0], 2))

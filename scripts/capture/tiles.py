# python3 tiles.py <tiledir> <out.png> <height>: stitch viewport tiles named NNN-<scrollY>.png
import sys, glob, os
from PIL import Image
d, out, h = sys.argv[1], sys.argv[2], int(sys.argv[3])
fs = sorted(glob.glob(d + "/*.png"))
first = Image.open(fs[0]); W = first.width
im = Image.new("RGB", (W, h), "white")
for f in fs:
    y = int(os.path.basename(f).split("-")[1].split(".")[0])
    im.paste(Image.open(f).convert("RGB"), (0, y))
im.save(out)

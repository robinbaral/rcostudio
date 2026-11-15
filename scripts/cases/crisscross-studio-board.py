# Puzzle Studio captures (scripts/cases/crisscross-studio-capture.mjs, 1440x900 at 2x)
# side by side on the warm grey of the other case boards (one capture fills the width).
# Usage: python3 crisscross-studio-board.py <capture dir> <out.png> word-list [grids ...]
import sys
from PIL import Image, ImageDraw, ImageFilter
src, out, *names = sys.argv[1:]
BG = (242, 241, 238); W = 2880; PAD_X, PAD_Y, GAP = 240, 140, 80
tw = (W - 2 * PAD_X - GAP * (len(names) - 1)) // len(names)
shots = []
for n in names:
    im = Image.open(f"{src}/studio-{n}.png").convert("RGB")
    shots.append(im.resize((tw, round(im.height * tw / im.width)), Image.LANCZOS))
th = shots[0].height
canvas = Image.new("RGB", (W, th + 2 * PAD_Y), BG)
x = PAD_X
for im in shots:
    sh = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((x, PAD_Y + 16, x + tw, PAD_Y + th + 16), 16, fill=60)
    canvas.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(30)))
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, tw - 1, th - 1), 16, fill=255)
    canvas.paste(im, (x, PAD_Y), m)
    ImageDraw.Draw(canvas).rounded_rectangle((x, PAD_Y, x + tw - 1, PAD_Y + th - 1), 16, outline=(222, 221, 217), width=2)
    x += tw + GAP
canvas.save(out, optimize=True)
print(canvas.size)

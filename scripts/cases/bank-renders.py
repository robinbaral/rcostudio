# Banking App slides from Robin's phone renders (transparent PNGs, 3200–4500px) in
# "Co-operative Bank App/03_Files/", in place of cropped Behance boards. Each render is
# trimmed to its content (shadow included) and centred on a plain background, at 16:10:
# the boards' light grey, or black for dark mode. A slide can sit lower than centre.
# Usage: python3 scripts/cases/bank-renders.py   (from rco-website/, needs Pillow)
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT.parents[2] / "Co-operative Bank App/03_Files"
OUT = ROOT / "src/assets/work"
W, H = 2880, 1800
LIGHT = (249, 249, 249)  # the Behance boards' background
DARK = (0, 0, 0)  # the dark mode board's background
FILL = 0.88  # share of the slide height the phones take up

# (render name in 03_Files, without "HERO-iPhone-X-" and ".png"; output name; background;
#  shift down from centre, as a share of the slide height)
SLIDES = [
    ("Vertikal-*-Home", "banking-app-balance", LIGHT, 0.05),
    ("Angle-3-*-Dark-Mode", "banking-app-dark", DARK, 0),
]

for pattern, name, bg, shift in SLIDES:
    (path,) = SRC.glob(f"HERO-iPhone-X-{pattern}.png")
    img = Image.open(path).convert("RGBA")
    img = img.crop(img.split()[-1].getbbox())
    scale = min(H * FILL / img.height, W * 0.9 / img.width)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    out = Image.new("RGB", (W, H), bg)
    out.paste(img, ((W - img.width) // 2, (H - img.height) // 2 + round(H * shift)), img)
    out.save(OUT / f"{name}.png", optimize=True)
    print(name, path.name, "->", out.size)

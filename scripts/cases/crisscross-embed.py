# Copies the playable puzzle from the CrissCross website's build into a standalone page for
# the case study (public/embeds/crisscross-puzzle/), shown there in an iframe.
#
#   cd ~/Projects/CrissCross/crisscross-website && npm run build
#   python3 scripts/cases/crisscross-embed.py ~/Projects/CrissCross/crisscross-website/dist
#
# Takes the demo's markup from dist/index.html, the two stylesheets (Tailwind and the Inter
# font), the demo script and its one import, the Latin font file and the sounds, into
# public/embeds/crisscross-puzzle/, with the page beside them as crisscross-puzzle.html.
# Paths are absolute (BASE): the live site drops trailing slashes, so relative ones break.
# The page tells its parent its height
# (postMessage "crisscross-puzzle-height", also in answer to "crisscross-puzzle-ping") so the
# iframe fits the layout at every width.
import re, shutil, sys
from pathlib import Path

dist = Path(sys.argv[1]).expanduser()
BASE = "/embeds/crisscross-puzzle/"
out = Path(__file__).resolve().parents[2] / "public/embeds/crisscross-puzzle"
page_file = out.parent / "crisscross-puzzle.html"
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)

html = (dist / "index.html").read_text()

# The demo root: the first element with data-puzzle-root, up to its matching </div>.
start = html.rfind("<div", 0, html.index("data-puzzle-root"))
depth, i = 0, start
for m in re.finditer(r"<div\b|</div>", html[start:]):
    depth += 1 if m.group() != "</div>" else -1
    if depth == 0:
        end = start + m.end()
        break
demo = html[start:end]

css = [h.split("/")[-1] for h in re.findall(r'<link rel="stylesheet" href="(/_astro/[^"]+\.css)"', html)]
js = re.search(r'<script type="module" src="/_astro/(PuzzleDemo[^"]+\.js)"', html).group(1)

for name in css:
    text = (dist / "_astro" / name).read_text().replace("url(/_astro/", f"url({BASE}")
    (out / name).write_text(text)
for font in re.findall(r"url\(" + re.escape(BASE) + r"(inter-latin-wght[^)]+)\)", "".join((out / n).read_text() for n in css)):
    shutil.copy(dist / "_astro" / font, out / font)

script = (dist / "_astro" / js).read_text().replace("`/sounds/", f"`{BASE}sounds/")
(out / js).write_text(script)
for imp in re.findall(r'from"\./([^"]+\.js)"', script):
    shutil.copy(dist / "_astro" / imp, out / imp)
shutil.copytree(dist / "sounds", out / "sounds")

links = "\n".join(f'<link rel="stylesheet" href="{BASE}{n}">' for n in css)
page = f"""<!doctype html>
<html lang="en" style="color-scheme: light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>CrissCross puzzle</title>
{links}
<style>
  html, body {{ margin: 0; background: transparent; overflow: hidden; }}
  body {{ padding: 0; container-type: inline-size; }}
  /* The case page draws the panel (full width, like the other images), so the demo's own
     rounded grey card is switched off here. */
  .puzzle-demo {{ background: transparent !important; border-radius: 0 !important; }}
</style>
</head>
<body>
{demo}
<script type="module" src="{BASE}{js}"></script>
<script>
  // Tell the case page how tall the puzzle is, so the iframe fits it: on load, on every
  // resize, and whenever the page asks (it may start listening after the first report).
  const post = () => parent.postMessage({{ type: "crisscross-puzzle-height", height: document.body.offsetHeight }}, "*");
  new ResizeObserver(post).observe(document.body);
  addEventListener("load", post);
  addEventListener("message", (e) => {{ if (e.data?.type === "crisscross-puzzle-ping") post(); }});
</script>
</body>
</html>
"""
page_file.write_text(page)
print("wrote", page_file, sorted(p.name for p in out.iterdir()))

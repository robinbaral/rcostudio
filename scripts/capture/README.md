# Capturing project screenshots

Tools used to make the 2x sources in `src/assets/work/` (Chrome DevTools Protocol on
Playwright's headless shell, `~/Library/Caches/ms-playwright/chromium_headless_shell-1148`).

- `node cap.mjs clips <url> <outdir> '<json>' [mobile]`: 1440x900 (or 390x844 with `mobile`)
  at 2x, one PNG per item. Items: `{name, y}` for a scroll offset; `{name, text}` to frame the
  section containing that text (everything else hidden, centred if it fits, else 40px above);
  `{name, at, fit: 1}` to frame the largest block under the screen centre at offset `at`.
  Options: `keepFixed` (keep fixed headers), `alignTop`, `pad`, `bg`, `halves` (two half-height
  shots, for pages that hang Chrome on a full 2x frame; join them afterwards). Env: `PREP`
  (JS run after load, e.g. hide cookie banners), `NOWALK` (skip the scroll through the page),
  `PORT`, `TIMEOUT`.
- `node cap.mjs full <url> <tiledir> [mobile]` then `python3 tiles.py <tiledir> <out.png>
  <height>`: a full-page capture at 1x, stitched from viewport tiles.
- `python3 match.py <full.png> <old.webp> ...`: finds where an existing shot sits on that page
  (scroll offset and mean difference; under ~6 is a match), to recapture the same framing.

Hero previews stretch the site's first section to fill the screen first (via `PREP`); the
composites (CrissCross devices, Pindrop App Store trio) are drawn with Pillow from each
project's own source files. See the git history of `src/assets/work/` for when each was made.

// Project rows: a desktop screenshot follows the cursor while hovering a row. The row shows its
// first (hero) image; only the thumbnail strip after the name (.project__thumb) switches it:
// the thumbnail under the cursor picks from the row's images (data-previews: the preview, then
// the gallery) and is marked as active. Back on the rest of the row, the hero image returns.
(function () {
  if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;

  var preview = document.querySelector(".preview");
  var img = preview.querySelector(".preview__img");
  var rows = document.querySelectorAll(".project[data-preview]");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var OFFSET = 24;
  var x = 0, y = 0, tx = 0, ty = 0, raf = 0;

  // Match the card to the image's own proportions, so nothing gets cropped
  // (site screenshots are 16:10, PDF pages 16:9, app shots portrait).
  function fit() {
    if (img.naturalWidth) preview.style.aspectRatio = img.naturalWidth + " / " + img.naturalHeight;
  }
  img.addEventListener("load", fit);

  // Each row's hover colour comes from its thumbnail: the most common strong hue, then
  // darkened or lightened until it reads against the section background (3:1, large text).
  var section = document.querySelector(".projects");

  function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2, h = 0, s = 0;
    if (max !== min) {
      var d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      h = max === r ? (g - b) / d + (g < b ? 6 : 0) : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
      h /= 6;
    }
    return [h, s, l];
  }

  function hslToRgb(h, s, l) {
    function f(n) {
      var k = (n + h * 12) % 12, a = s * Math.min(l, 1 - l);
      return Math.round(255 * (l - a * Math.max(-1, Math.min(k - 3, 9 - k, 1))));
    }
    return [f(0), f(8), f(4)];
  }

  function hexToRgb(hex) {
    var n = parseInt(hex.replace("#", ""), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }

  function luminance(c) {
    var v = c.map(function (x) { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); });
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
  }

  function contrast(a, b) {
    var la = luminance(a), lb = luminance(b);
    return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
  }

  function sample(image) {
    var c = document.createElement("canvas"), w = 160, h = Math.max(1, Math.round(160 * image.naturalHeight / image.naturalWidth));
    c.width = w; c.height = h;
    var ctx = c.getContext("2d", { willReadFrequently: true });
    ctx.drawImage(image, 0, 0, w, h);
    var px = ctx.getImageData(0, 0, w, h).data, bins = [], i, k;
    for (k = 0; k < 24; k++) bins.push({ weight: 0, r: 0, g: 0, b: 0, n: 0 });
    for (i = 0; i < px.length; i += 4) {
      var hsl = rgbToHsl(px[i], px[i + 1], px[i + 2]);
      if (hsl[1] < 0.35 || hsl[2] < 0.15 || hsl[2] > 0.92) continue; // skip greys, near-black, near-white
      var bin = bins[Math.floor(hsl[0] * 24) % 24];
      bin.weight += hsl[1] * hsl[1]; // favour vivid accents over large muted areas
      bin.r += px[i]; bin.g += px[i + 1]; bin.b += px[i + 2]; bin.n++;
    }
    var best = bins.reduce(function (a, b) { return b.weight > a.weight ? b : a; });
    // Black-and-white thumbnails (e.g. Pindrop) have no strong hue: keep the normal text colour.
    if (best.n < w * h * 0.0015) return null;
    return [best.r / best.n, best.g / best.n, best.b / best.n];
  }

  function readable(rgb, bg, exact) {
    var hsl = rgbToHsl(rgb[0], rgb[1], rgb[2]), step = luminance(bg) > 0.5 ? -0.02 : 0.02;
    // Keep the hue, but lift muddy or washed-out samples to a clean mid-tone first.
    // A colour named on the row (exact) is left alone unless it fails the contrast check.
    if (!exact) {
      hsl[1] = Math.max(hsl[1], 0.55);
      hsl[2] = Math.min(Math.max(hsl[2], 0.42), 0.6);
    }
    var out = exact ? rgb.map(Math.round) : hslToRgb(hsl[0], hsl[1], hsl[2]);
    for (var n = 0; n < 50 && contrast(out, bg) < 3; n++) {
      hsl[2] = Math.min(1, Math.max(0, hsl[2] + step));
      out = hslToRgb(hsl[0], hsl[1], hsl[2]);
    }
    return "rgb(" + out.join(",") + ")";
  }

  function paint() {
    var bg = getComputedStyle(section).backgroundColor.match(/\d+/g).slice(0, 3).map(Number);
    rows.forEach(function (row) {
      // A row can name its own colour (data-accent): used as given where it reads, darkened
      // or lightened just enough where it doesn't (e.g. a pale colour on the white section).
      var onDark = luminance(bg) < 0.5;
      // Separate colours per background are used exactly as given.
      if (row.dataset.accentOnDark) row.style.setProperty("--row-accent", onDark ? row.dataset.accentOnDark : row.dataset.accentOnLight);
      else if (row.dataset.accent) row.style.setProperty("--row-accent", readable(hexToRgb(row.dataset.accent), bg, true));
      else if (row._accent) row.style.setProperty("--row-accent", readable(row._accent, bg));
      else row.style.removeProperty("--row-accent");
    });
  }

  // Load every thumbnail up front: warms the cache for the first hover and gives us its colour.
  rows.forEach(function (row) {
    var im = new Image();
    im.onload = function () {
      try { row._accent = sample(im); } catch (err) { row._accent = null; }
      paint();
    };
    im.src = row.dataset.preview;
  });

  // The list follows the OS mode (light or dark): pick the colours again when it switches,
  // once the section's own colour transition (0.2s) has finished.
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
    window.setTimeout(paint, 250);
  });


  function target(e) {
    var w = preview.offsetWidth, h = preview.offsetHeight;
    // Sit right of the cursor; flip left near the edge, keep inside the viewport vertically.
    // Over the thumbnail strip, sit past its end instead, so no thumbnail is covered.
    var from = e.clientX;
    if (thumbs.length && overThumb(e) >= 0) from = thumbs[thumbs.length - 1].getBoundingClientRect().right;
    tx = from + OFFSET + w > window.innerWidth ? e.clientX - OFFSET - w : from + OFFSET;
    ty = Math.min(Math.max(e.clientY - h / 2, 16), window.innerHeight - h - 16);
  }

  function tick() {
    x += (tx - x) * 0.2;
    y += (ty - y) * 0.2;
    preview.style.transform = "translate3d(" + x + "px," + y + "px,0)";
    raf = Math.abs(tx - x) + Math.abs(ty - y) > 0.5 ? requestAnimationFrame(tick) : 0;
  }

  function move(e) {
    target(e);
    if (reduce) { x = tx; y = ty; preview.style.transform = "translate3d(" + x + "px," + y + "px,0)"; }
    else if (!raf) raf = requestAnimationFrame(tick);
  }

  var list = [], shown = 0, thumbs = [];

  function mark(i) {
    thumbs.forEach(function (t, k) { t.classList.toggle("is-active", k === i); });
  }

  function show(i) {
    if (i === shown) return;
    shown = i;
    img.src = list[i];
    mark(i);
  }

  // The thumbnail under the cursor (gaps between thumbnails count towards the nearer one), or -1
  // off the strip.
  function overThumb(e) {
    if (!thumbs.length) return -1;
    var first = thumbs[0].getBoundingClientRect(), last = thumbs[thumbs.length - 1].getBoundingClientRect();
    if (e.clientX < first.left || e.clientX > last.right) return -1;
    var best = 0, dist = Infinity;
    thumbs.forEach(function (t, k) {
      var r = t.getBoundingClientRect(), d = Math.abs(e.clientX - (r.left + r.width / 2));
      if (d < dist) { dist = d; best = k; }
    });
    return best;
  }

  function scrub(e) {
    if (list.length < 2) return;
    var i = overThumb(e);
    show(i >= 0 ? i : 0);
  }

  rows.forEach(function (row) {
    row.addEventListener("mouseenter", function (e) {
      list = (row.dataset.previews || row.dataset.preview).split(",");
      thumbs = Array.prototype.slice.call(row.querySelectorAll(".project__thumb"));
      shown = 0;
      mark(0);
      // Warm the rest of this row's images, so the thumbnails don't wait on the network.
      if (!row._warmed) {
        row._warmed = true;
        list.slice(1).forEach(function (src) { new Image().src = src; });
      }
      img.src = row.dataset.preview;
      preview.classList.toggle("preview--portrait", row.dataset.previewShape === "portrait");
      fit();
      target(e);
      if (!preview.classList.contains("is-visible")) { x = tx; y = ty; preview.style.transform = "translate3d(" + x + "px," + y + "px,0)"; }
      preview.classList.add("is-visible");
    });
    row.addEventListener("mousemove", function (e) {
      move(e);
      scrub(e);
    });
    row.addEventListener("mouseleave", function () { preview.classList.remove("is-visible"); });
  });
})();

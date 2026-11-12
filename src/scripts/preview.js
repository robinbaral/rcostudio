// Project rows: a desktop screenshot follows the cursor while hovering a row.
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

  // The section flips colours with the OS theme, so re-check contrast when that changes.
  var scheme = window.matchMedia("(prefers-color-scheme: dark)");
  if (scheme.addEventListener) scheme.addEventListener("change", function () { setTimeout(paint, 250); });

  function target(e) {
    var w = preview.offsetWidth, h = preview.offsetHeight;
    // Sit right of the cursor; flip left near the edge, keep inside the viewport vertically.
    tx = e.clientX + OFFSET + w > window.innerWidth ? e.clientX - OFFSET - w : e.clientX + OFFSET;
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

  rows.forEach(function (row) {
    row.addEventListener("mouseenter", function (e) {
      img.src = row.dataset.preview;
      preview.classList.toggle("preview--portrait", row.dataset.previewShape === "portrait");
      fit();
      target(e);
      if (!preview.classList.contains("is-visible")) { x = tx; y = ty; preview.style.transform = "translate3d(" + x + "px," + y + "px,0)"; }
      preview.classList.add("is-visible");
    });
    row.addEventListener("mousemove", move);
    row.addEventListener("mouseleave", function () { preview.classList.remove("is-visible"); });
  });
})();

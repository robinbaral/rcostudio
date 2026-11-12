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

  // Warm the cache so the first hover doesn't flash empty.
  rows.forEach(function (row) { new Image().src = row.dataset.preview; });

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

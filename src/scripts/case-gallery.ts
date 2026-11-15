// Gallery: a scroll-snap strip with previous/next buttons; the caption and the count follow
  // the image in view.
  document.querySelectorAll<HTMLElement>("[data-gallery]").forEach((gallery) => {
    const track = gallery.querySelector<HTMLElement>(".gallery__track")!;
    const slides = Array.from(track.querySelectorAll<HTMLElement>(".gallery__slide"));
    const caption = gallery.querySelector(".gallery__caption")!;
    const index = gallery.querySelector("[data-gallery-index]")!;
    const prev = gallery.querySelector<HTMLButtonElement>("[data-gallery-prev]")!;
    const next = gallery.querySelector<HTMLButtonElement>("[data-gallery-next]")!;
    let current = 0;

    const update = () => {
      current = Math.round(track.scrollLeft / track.clientWidth);
      caption.textContent = slides[current]?.dataset.caption ?? "";
      index.textContent = String(current + 1);
      prev.disabled = current === 0;
      next.disabled = current === slides.length - 1;
    };
    const go = (i: number) => track.scrollTo({ left: i * track.clientWidth });

    prev.addEventListener("click", () => go(current - 1));
    next.addEventListener("click", () => go(current + 1));
    track.addEventListener("scroll", () => requestAnimationFrame(update), { passive: true });
    track.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") { e.preventDefault(); go(current + 1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); go(current - 1); }
    });
    update();
  });

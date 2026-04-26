document.addEventListener("DOMContentLoaded", () => {
  initCarousel();
});

function initCarousel() {
  const track = document.getElementById("carousel-track");

  if (!track) return;

  const slides = Array.from(track.querySelectorAll(".carousel-slide"));
  const nextBtn = document.getElementById("next-btn");
  const prevBtn = document.getElementById("prev-btn");
  const indicator = document.getElementById("carousel-indicator");

  if (slides.length === 0) return;

  if (slides.length <= 1) {
    if (nextBtn) nextBtn.style.display = "none";
    if (prevBtn) prevBtn.style.display = "none";
    if (indicator) indicator.style.display = "none";
    return;
  }

  const updateUI = () => {
    const slideWidth = slides[0].getBoundingClientRect().width;
    const currentIndex = Math.round(track.scrollLeft / slideWidth);

    if (indicator) {
      indicator.textContent = `${currentIndex + 1}/${slides.length}`;
    }

    if (prevBtn) {
      if (currentIndex === 0) {
        prevBtn.classList.add("hidden");
      } else {
        prevBtn.classList.remove("hidden");
      }
    }

    if (nextBtn) {
      if (currentIndex === slides.length - 1) {
        nextBtn.classList.add("hidden");
      } else {
        nextBtn.classList.remove("hidden");
      }
    }
  };

  track.addEventListener("scroll", () => {
    clearTimeout(track.scrollTimeout);
    track.scrollTimeout = setTimeout(updateUI, 50);
  });

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      const slideWidth = slides[0].getBoundingClientRect().width;
      track.scrollBy({ left: slideWidth, behavior: "smooth" });
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      const slideWidth = slides[0].getBoundingClientRect().width;
      track.scrollBy({ left: -slideWidth, behavior: "smooth" });
    });
  }

  updateUI();
}
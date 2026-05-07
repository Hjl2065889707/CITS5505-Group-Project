document.addEventListener("DOMContentLoaded", () => {
  initCarousel();
});

function initCarousel() {
  const track = document.getElementById("carousel-track");
  const slides = Array.from(track.querySelectorAll(".carousel-slide"));
  const nextBtn = document.getElementById("next-btn");
  const prevBtn = document.getElementById("prev-btn");
  const indicator = document.getElementById("carousel-indicator");

  if (!track || slides.length === 0) return;

  // Hide controls entirely if there's only 1 image
  if (slides.length <= 1) {
    if (nextBtn) nextBtn.style.display = 'none';
    if (prevBtn) prevBtn.style.display = 'none';
    if (indicator) indicator.style.display = 'none';
    return;
  }

  const updateUI = () => {
    // Determine current index by checking the scroll position
    const slideWidth = slides[0].getBoundingClientRect().width;
    // Calculate which slide we are mostly viewing
    const currentIndex = Math.round(track.scrollLeft / slideWidth);

    // Update indicator text (e.g., 1/2)
    if (indicator) {
      indicator.textContent = `${currentIndex + 1}/${slides.length}`;
    }

    // Toggle visibility of Previous button
    if (currentIndex === 0) {
      prevBtn.classList.add('hidden');
    } else {
      prevBtn.classList.remove('hidden');
    }

    // Toggle visibility of Next button
    if (currentIndex === slides.length - 1) {
      nextBtn.classList.add('hidden');
    } else {
      nextBtn.classList.remove('hidden');
    }
  };

  // Listen to the scroll event so the UI updates even if the user swipes instead of clicking
  track.addEventListener('scroll', () => {
    // Debounce to improve performance
    clearTimeout(track.scrollTimeout);
    track.scrollTimeout = setTimeout(updateUI, 50);
  });

  // Handle button clicks to programmatically scroll
  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      const slideWidth = slides[0].getBoundingClientRect().width;
      track.scrollBy({ left: slideWidth, behavior: 'smooth' });
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      const slideWidth = slides[0].getBoundingClientRect().width;
      track.scrollBy({ left: -slideWidth, behavior: 'smooth' });
    });
  }

  // Set initial state
  updateUI();
}

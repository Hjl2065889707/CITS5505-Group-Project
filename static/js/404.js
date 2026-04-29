document.addEventListener("DOMContentLoaded", () => {
  initBackButton();
});

function initBackButton() {
  const backButton = document.getElementById("go-back-btn");

  if (!backButton) return;

  backButton.addEventListener("click", () => {
    if (window.history.length > 1) {
      window.history.back();
    } else {
      window.location.href = "../main/index.html";
    }
  });
}
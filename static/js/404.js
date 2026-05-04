document.addEventListener("DOMContentLoaded", () => {
  initBackButton();
});

function initBackButton() {
  const backButton = document.getElementById("go-back-btn");

  if (!backButton) return;

  backButton.addEventListener("click", () => {
    if (hasSameOriginReferrer()) {
      window.history.back();
    } else {
      window.location.href = "/";
    }
  });
}

function hasSameOriginReferrer() {
  if (!document.referrer) return false;

  try {
    const referrerUrl = new URL(document.referrer);
    return referrerUrl.origin === window.location.origin;
  } catch {
    return false;
  }
}
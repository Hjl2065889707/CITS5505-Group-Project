document.addEventListener("DOMContentLoaded", () => {
  // Initialise 404 back button when page loads
  initBackButton();
});

function initBackButton() {
  // Find the Go Back button
  const backButton = document.getElementById("go-back-btn");

  if (!backButton) return;

  // Handle safe back navigation
  backButton.addEventListener("click", () => {
    if (hasSameOriginReferrer()) {
      window.history.back();
    } else {
      window.location.href = "/";
    }
  });
}

function hasSameOriginReferrer() {
  // No referrer means there is no safe page to go back to
  if (!document.referrer) return false;

  try {
    // Only allow back navigation inside the same website
    const referrerUrl = new URL(document.referrer);
    return referrerUrl.origin === window.location.origin;
  } catch {
    return false;
  }
}
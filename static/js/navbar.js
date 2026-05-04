/**
 * Navbar toggle — mobile hamburger menu.
 * Toggles the .is-open class on the nav links container.
 */
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".site-navbar__toggle");
  const links = document.querySelector(".site-navbar__links");

  if (!toggle || !links) return;

  toggle.addEventListener("click", () => {
    const isOpen = links.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });
});
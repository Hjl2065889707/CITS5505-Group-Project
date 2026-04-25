document.addEventListener("DOMContentLoaded", () => {
  renderNavbar();
});

function renderNavbar() {
  const navbarMount = document.getElementById("site-navbar");

  if (!navbarMount) return;

  const basePath = navbarMount.dataset.basePath || "..";
  const activePage = navbarMount.dataset.active || "";

  const links = [
    {
      key: "home",
      label: "Feed",
      href: `${basePath}/main/index.html`,
    },
    {
      key: "map",
      label: "Map",
      href: `${basePath}/map/index.html`,
    },
    {
      key: "post",
      label: "Post",
      href: `${basePath}/post/index.html`,
    },
    {
      key: "profile",
      label: "Profile",
      href: `${basePath}/profile/index.html`,
    },
  ];

  const navLinksHtml = links
    .map((link) => {
      const activeClass = link.key === activePage ? "active" : "";

      return `
        <a class="site-navbar__link ${activeClass}" href="${link.href}">
          ${link.label}
        </a>
      `;
    })
    .join("");

  navbarMount.innerHTML = `
    <nav class="site-navbar" aria-label="Main navigation">
      <div class="site-navbar__inner">
        <a class="site-navbar__brand" href="${basePath}/main/index.html">
          <span class="site-navbar__logo" aria-hidden="true">🎣</span>
          <span>CatchLog</span>
        </a>

        <button
          class="site-navbar__toggle"
          type="button"
          aria-label="Toggle navigation menu"
          aria-expanded="false"
        >
          ☰
        </button>

        <div class="site-navbar__links">
          ${navLinksHtml}
        </div>

        <div class="site-navbar__actions">
          <a class="site-navbar__login" href="${basePath}/login/index.html">
            Login
          </a>
        </div>
      </div>
    </nav>
  `;

  const toggleButton = navbarMount.querySelector(".site-navbar__toggle");
  const navLinks = navbarMount.querySelector(".site-navbar__links");

  if (!toggleButton || !navLinks) return;

  toggleButton.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("is-open");
    toggleButton.setAttribute("aria-expanded", String(isOpen));
  });
}
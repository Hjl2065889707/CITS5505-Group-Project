import { posts } from "./data.js";

import { openSidebar, closeSidebar, showEmptySidebar } from "./sidebar.js";

import { groupPosts } from "./utils.js";

function createMarkerIcon(count) {
  return L.divIcon({
    className: "custom-marker",
    html: `
      <div class="marker-pin">
        ${count > 1 ? `<span class="marker-count">${count}</span>` : ""}
      </div>
    `,
    iconSize: [30, 30],
    iconAnchor: [15, 38]
  });
}

function updateTabDirection() {
  sidebarTab.textContent = sidebar.classList.contains("open") ? "❮" : "❯";
}

let lastOpenedGroup = null;

// Initialize map
const map = L.map('map', {
  zoomControl: false
}).setView([-31.9523, 115.8613], 13);

// Add zoom control to TOP RIGHT
L.control.zoom({ position: 'topright' }).addTo(map);

// Add tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
}).addTo(map);

// Sidebar
const sidebar = document.getElementById("sidebar");

const sidebarTab = document.getElementById("sidebar-tab");

sidebarTab.addEventListener("click", () => {

  if (sidebar.classList.contains("open")) {
    closeSidebar(sidebar);   // ✅ FIXED
    updateTabDirection();    // ✅ add this
    return;
  }

  if (lastOpenedGroup) {
    openSidebar(lastOpenedGroup, sidebar, closeSidebar);  // ✅ FIXED
  } else {
    showEmptySidebar(sidebar, closeSidebar);  // ✅ FIXED
  }

  updateTabDirection();   // ✅ add this
});

// marker rendering
const groups = groupPosts(posts);

groups.forEach(group => {
  const { lat, lng } = group[0];

  const marker = L.marker([lat, lng], {
    icon: createMarkerIcon(group.length)
  }).addTo(map);

  marker.on("click", (e) => {
  L.DomEvent.stopPropagation(e);

  lastOpenedGroup = group;

  openSidebar(group, sidebar, closeSidebar);
  updateTabDirection();   // ✅ ADD THIS
});
});


// Click map → close
map.on("click", () => {
  closeSidebar(sidebar);   // ✅ FIXED
  updateTabDirection();    // ✅ ADD THIS
});
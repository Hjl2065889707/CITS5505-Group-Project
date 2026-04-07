import { posts } from "./data.js";

import { openSidebar, closeSidebar, showEmptySidebar } from "./sidebar.js";

import { groupPosts } from "./utils.js";

import { renderMarkers } from "./marker.js";


function updateTabDirection() {
  sidebarTab.textContent = sidebar.classList.contains("open") ? "❮" : "❯";
}

function openSidebarWithUI(group) {
  openSidebar(group, sidebar, closeSidebar);
  updateTabDirection();
}

function closeSidebarWithUI() {
  closeSidebar(sidebar);
  updateTabDirection();
}



// Initialize map
const map = L.map('map', {
  zoomControl: false
}).setView([-31.9523, 115.8613], 13);

// Add zoom control to TOP RIGHT
L.control.zoom({ position: 'topright' }).addTo(map);

// Add tiles
L.tileLayer(
  'https://tiles.stadiamaps.com/tiles/stamen_toner_dark/{z}/{x}/{y}{r}.png',
  {
    attribution: '&copy; OpenStreetMap contributors &copy; Stadia Maps',
    maxZoom: 20
  }
).addTo(map);



// Sidebar

let lastOpenedGroup = null;

const sidebar = document.getElementById("sidebar");

const sidebarTab = document.getElementById("sidebar-tab");

sidebarTab.addEventListener("click", () => {

  if (sidebar.classList.contains("open")) {
    closeSidebarWithUI();
    return;
  }

  if (lastOpenedGroup) {
    openSidebarWithUI(lastOpenedGroup);
  } else {
    showEmptySidebar(sidebar, closeSidebar);
    updateTabDirection(); 
  }
});


// Markers Rendering

let markerLayer = L.layerGroup().addTo(map);

function renderMarkersDynamic() {
  markerLayer.clearLayers();

  const zoom = map.getZoom();

  const threshold =
    zoom >= 15 ? 30 :
    zoom >= 13 ? 50 :
    80;

  const groups = groupPosts(posts, threshold);

  renderMarkers(markerLayer, groups, (group) => {
    lastOpenedGroup = group;
    openSidebar(group, sidebar, closeSidebar);
    updateTabDirection();
  });
}

renderMarkersDynamic();

map.on("zoomend", renderMarkersDynamic);


// Click map → close
map.on("click", () => {
  closeSidebarWithUI();
});
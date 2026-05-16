import { openSidebar, closeSidebar, showEmptySidebar } from "./sidebar.js";

import { groupPosts } from "./utils.js";

import { renderMarkers } from "./marker.js";


function updateTabDirection() {
  sidebarTab.textContent = sidebar.classList.contains("open") ? "❮" : "❯";
}

function openSidebarWithUI(group) {
  lastOpenedGroup = group;
  selectedPostId = group[0].id;
  openSidebar(group, sidebar, closeSidebar);
  updateTabDirection();
  renderMarkersDynamic();
}

function closeSidebarWithUI() {
  closeSidebar(sidebar);
  selectedPostId = null;
  updateTabDirection();
  renderMarkersDynamic();
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

let posts = [];
let lastOpenedGroup = null;
let selectedPostId = null;

const sidebar = document.getElementById("sidebar");

const sidebarTab = document.getElementById("sidebar-tab");

sidebarTab.addEventListener("click", () => {

  if (sidebar.classList.contains("open")) {
    closeSidebarWithUI();
    return;
  }

  if (lastOpenedGroup) {
  selectedPostId = lastOpenedGroup[0].id;
  openSidebarWithUI(lastOpenedGroup);
  renderMarkersDynamic();
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
    selectedPostId = group[0].id;
    openSidebar(group, sidebar, closeSidebar);
    updateTabDirection();
    renderMarkersDynamic();
  }, selectedPostId);
}

async function loadMapPosts() {
  try {
    const response = await fetch("/api/posts/map");

    if (!response.ok) {
      throw new Error(`Failed to load map posts: ${response.status}`);
    }

    posts = await response.json();
    renderMarkersDynamic();
  } catch (error) {
    console.error("Map posts load failed:", error);
    showEmptySidebar(sidebar, closeSidebar);
    sidebar.querySelector(".sidebar-feed").innerHTML = `
      <p style="padding: 10px; color: #666;">
        Failed to load map posts.
      </p>
    `;
    updateTabDirection();
  }
}

async function refreshMapPostsAndSidebar() {
  const wasSidebarOpen = sidebar.classList.contains("open");

  const previouslyOpenPostIds = lastOpenedGroup
    ? lastOpenedGroup.map(post => String(post.id))
    : [];

  await loadMapPosts();

  if (!wasSidebarOpen || previouslyOpenPostIds.length === 0) {
    return;
  }

  const refreshedGroup = posts.filter(post =>
    previouslyOpenPostIds.includes(String(post.id))
  );

  if (refreshedGroup.length > 0) {
    lastOpenedGroup = refreshedGroup;
    selectedPostId = refreshedGroup[0].id;
    openSidebarWithUI(refreshedGroup);
  }
}

map.on("zoomend", renderMarkersDynamic);

// Click map → close
map.on("click", () => {
  closeSidebarWithUI();
});

document.addEventListener("postInteractionChanged", async (event) => {
  const changedPostId = String(event.detail.postId);

  const changedPostIsOnMap = posts.some(post =>
    String(post.id) === changedPostId
  );

  if (!changedPostIsOnMap) {
    return;
  }

  await refreshMapPostsAndSidebar();
});

loadMapPosts();
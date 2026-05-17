// Open the sidebar and insert the compact post-card HTML returned by the backend.
// This keeps map sidebar cards visually consistent with feed/profile post cards.
export function openSidebar(group, sidebar, closeSidebar) {
  sidebar.innerHTML = `
    <div class="sidebar-header">
      <h2>Posts</h2>
    </div>

    <div class="sidebar-feed">
      ${group.map(post => post.html).join("")}
    </div>
  `;

  sidebar.classList.add("open");
}

// Closes the Sidebar
export function closeSidebar(sidebar) {
  sidebar.classList.remove("open");
}

// Show an initial helper message before the user clicks a map marker.
export function showEmptySidebar(sidebar, closeSidebar) {
  sidebar.innerHTML = `
    <div class="sidebar-header">
      <h2>Welcome</h2>
    </div>

    <div class="sidebar-feed">
      <p style="padding: 10px; color: #666;">
        Get started: click on a marker to view posts.
      </p>
    </div>
  `;

  sidebar.classList.add("open");
}
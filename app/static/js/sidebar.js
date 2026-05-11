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

export function closeSidebar(sidebar) {
  sidebar.classList.remove("open");
}

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
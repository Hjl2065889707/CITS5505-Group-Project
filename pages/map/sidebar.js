export function openSidebar(group) {
    group.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

    sidebar.innerHTML = `
    <div class="sidebar-header">
    <button id="closeBtn">←</button>
    <h2>Posts</h2>
    </div>

    <div class="sidebar-feed">
    ${group.map(post => renderPost(post)).join("")}
    </div>
    `;

    sidebar.classList.add("open");
    updateTabDirection();

    document.getElementById("closeBtn")
    .addEventListener("click", closeSidebar);
}

export function renderPost(post) {
  return `
    <div class="post-card">

      <div class="post-header">
        <div>
          <div class="username">${post.user}</div>
          <div class="time">${formatTime(post.createdAt)}</div>
        </div>
      </div>

      <div class="post-body">
        <p class="post-text">${post.description}</p>
        ${post.image ? `<img src="${post.image}" class="post-img">` : ""}
      </div>

      <div class="post-footer">
        <button class="action-btn">👍 Like</button>
        <button class="action-btn">💬 Comment</button>
      </div>

    </div>
  `;
}

// Close sidebar
export function closeSidebar() {
  sidebar.classList.remove("open");
  updateTabDirection();
}

export function showEmptySidebar() {
  sidebar.innerHTML = `
    <div class="sidebar-header">
      <button id="closeBtn">←</button>
      <h2>Welcome</h2>
    </div>

    <div class="sidebar-feed">
      <p style="padding: 10px; color: #666;">
        Get started: click on a marker to view posts.
      </p>
    </div>
  `;

  sidebar.classList.add("open");

  document.getElementById("closeBtn")
    .addEventListener("click", closeSidebar);
}

export function formatTime(dateStr) {
  if (!dateStr) return "";

  const diff = (Date.now() - new Date(dateStr)) / 1000;

  if (diff < 3600) return Math.floor(diff / 60) + "m ago";
  if (diff < 86400) return Math.floor(diff / 3600) + "h ago";

  return "1d ago";
}

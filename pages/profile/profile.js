let myPosts = [];
let savedPosts = []; // Add variable for saved posts

document.addEventListener("DOMContentLoaded", () => {
  const navTabs = document.querySelectorAll(".nav-tab");
  const tabContents = document.querySelectorAll(".tab-content");

  navTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      // Remove active class from all tabs and contents
      navTabs.forEach((t) => t.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));

      // Add active class to clicked tab
      tab.classList.add("active");

      // Show corresponding tab content
      const targetId = tab.getAttribute("data-target");
      document.getElementById(targetId).classList.add("active");
    });
  });

  // Fetch and render both sets of posts
  loadPosts("../../mockdata/myPosts.json", "my-posts").then(
    (data) => (myPosts = data),
  );
  loadPosts("../../mockdata/savedPosts.json", "saved-posts").then(
    (data) => (savedPosts = data),
  );
});

async function loadPosts(url, containerId) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const posts = await response.json();
    renderPostsGrid(posts, containerId);
    return posts;
  } catch (error) {
    console.error(`Failed to fetch posts from ${url}:`, error);
    document.getElementById(containerId).innerHTML =
      `<p>Error loading posts.</p>`;
    return [];
  }
}

function renderPostsGrid(posts, containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = ""; // Clear existing content

  if (posts.length === 0) {
    container.innerHTML = `<p>You haven't posted anything yet.</p>`;
    return;
  }

  const feedContainer = document.createElement("div");
  feedContainer.className = "feed-container";

  posts.forEach((post) => {
    // Only use the first photo for the thumbnail
    const photos = post.photos && post.photos.length > 0 ? post.photos : "";

    // Format the date simply for now
    const dateStr = new Date(post.createdAt).toLocaleDateString();

    const postElement = document.createElement("div");
    postElement.className = "feed-card";

    // Build internal HTML for the feed card
    let htmlContent = `
      <div class="feed-header">
        <img src="${post.author.avatarUrl}" alt="Author avatar" class="feed-avatar" />
        <div class="feed-user-info">
          <div class="feed-username">${post.author.username}</div>
          <div class="feed-time">${dateStr}</div>
        </div>
      </div>
      <div class="feed-content">${post.content}</div>
    `;

    // Only append image if one exists
    if (photos && photos.length > 0) {
      htmlContent += `<div class="feed-image-grid">`;
      photos.forEach((photo) => {
        htmlContent += `
          <a href="../post/index.html?id=${post.id}" class="image-link">
            <img src="${photo}" alt="Post image" class="feed-image-thumb" />
          </a>
        `;
      });
      htmlContent += `</div>`;
    }

    // Add footer
    htmlContent += `
      <div class="feed-footer">
        <span class="feed-metric">❤️ ${post.metrics.likes} Likes</span>
        <span class="feed-metric">💬 ${post.metrics.commentsCount} Comments</span>
      </div>
    `;

    postElement.innerHTML = htmlContent;
    feedContainer.appendChild(postElement);
  });

  container.appendChild(feedContainer);
}

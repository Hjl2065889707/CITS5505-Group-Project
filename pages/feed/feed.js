let allPosts = [];
let currentSearch = "";
let currentTag = "All";

/* Load data: merge mock JSON + localStorage posts */
fetch("../../mockdata/feedPosts.json")
  .then(res => res.json())
  .then(jsonPosts => {
    const localPosts = JSON.parse(localStorage.getItem("userPosts") || "[]");
    allPosts = [...localPosts, ...jsonPosts];
    renderPosts(allPosts);
  })
  .catch(err => {
    console.error("Failed to load posts:", err);
    const localPosts = JSON.parse(localStorage.getItem("userPosts") || "[]");
    allPosts = localPosts;
    renderPosts(allPosts);
  });

/* Render */
function renderPosts(posts) {
  const container = document.getElementById("feedContainer");
  if (!container) return;

  container.innerHTML = "";

  if (!posts || posts.length === 0) {
    container.innerHTML =
      "<p style='text-align:center;color:#8e8e8e;padding:20px;'>No posts found</p>";
    return;
  }

  posts.forEach(post => {
    const card = document.createElement("div");
    card.className = "feed-card";

    const images = Array.isArray(post.images) ? post.images : [];

    card.innerHTML = `
      <div class="feed-header">
        <img class="feed-avatar" src="${post.avatar || ""}" alt="avatar"/>
        <div>
          <div class="feed-username">${post.username || ""}</div>
          <div style="font-size:12px;color:gray">${post.time || ""}</div>
        </div>
      </div>

      <div class="feed-content">
        ${post.content || ""}
      </div>

      ${
        images.length > 0
          ? `<div class="feed-image-grid">
              ${images.map(img => `<img src="${img}" alt="post image"/>`).join("")}
            </div>`
          : ""
      }

      <div class="feed-footer">
        <button class="action-btn like-btn" data-id="${post.id}">
          ❤️ <span class="like-count">${post.likes ?? 0}</span>
        </button>
        <button class="action-btn comment-btn" data-id="${post.id}">
          💬 <span class="comment-count">${post.comments ?? 0}</span>
        </button>
      </div>
    `;

    /* Like button */
    card.querySelector(".like-btn").addEventListener("click", function () {
      const span = this.querySelector(".like-count");
      const post = allPosts.find(p => String(p.id) === String(this.dataset.id));
      if (!post) return;

      if (this.classList.contains("liked")) {
        this.classList.remove("liked");
        post.likes = Math.max(0, (post.likes ?? 1) - 1);
      } else {
        this.classList.add("liked");
        post.likes = (post.likes ?? 0) + 1;
      }
      span.textContent = post.likes;
    });

    /* Comment button */
    card.querySelector(".comment-btn").addEventListener("click", function () {
      const input = prompt("Leave a comment:");
      if (input && input.trim()) {
        const span = this.querySelector(".comment-count");
        const post = allPosts.find(p => String(p.id) === String(this.dataset.id));
        if (!post) return;
        post.comments = (post.comments ?? 0) + 1;
        span.textContent = post.comments;
      }
    });

    container.appendChild(card);
  });
}

/* Apply both filters together */
function applyFilters() {
  let filtered = allPosts;

  if (currentTag !== "All") {
    filtered = filtered.filter(post =>
      Array.isArray(post.tags) && post.tags.includes(currentTag)
    );
  }

  if (currentSearch) {
    filtered = filtered.filter(post =>
      (post.content || "").toLowerCase().includes(currentSearch) ||
      (post.username || "").toLowerCase().includes(currentSearch)
    );
  }

  renderPosts(filtered);
}

/* Search */
const searchInput = document.getElementById("searchInput");
if (searchInput) {
  searchInput.addEventListener("input", () => {
    currentSearch = searchInput.value.toLowerCase();
    applyFilters();
  });
}

/* Tag filter */
const tagsEl = document.querySelectorAll(".tag");
tagsEl.forEach(tag => {
  tag.addEventListener("click", () => {
    document.querySelector(".tag.active")?.classList.remove("active");
    tag.classList.add("active");
    currentTag = tag.innerText;
    applyFilters();
  });
});

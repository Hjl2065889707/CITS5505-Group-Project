let allPosts = [];
let currentSearch = "";
let currentTag = "All";

/* Load data: merge mock JSON + localStorage posts */
fetch("../mockdata/feedPosts.json")
  .then(res => {
    if (!res.ok) {
      throw new Error(`Failed to load mock posts: ${res.status}`);
    }
    return res.json();
  })
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

  container.replaceChildren();

  if (!posts || posts.length === 0) {
    const emptyMessage = document.createElement("p");
    emptyMessage.style.textAlign = "center";
    emptyMessage.style.color = "#8e8e8e";
    emptyMessage.style.padding = "20px";
    emptyMessage.textContent = "No posts found";
    container.appendChild(emptyMessage);
    return;
  }

  posts.forEach(post => {
    const card = document.createElement("div");
    card.className = "feed-card";

    const images = Array.isArray(post.images) ? post.images : [];

    const header = document.createElement("div");
    header.className = "feed-header";

    const avatar = document.createElement("img");
    avatar.className = "feed-avatar";
    avatar.src = post.avatar || "";
    avatar.alt = "avatar";

    const headerText = document.createElement("div");

    const username = document.createElement("div");
    username.className = "feed-username";
    username.textContent = post.username || "";

    const time = document.createElement("div");
    time.style.fontSize = "12px";
    time.style.color = "gray";
    time.textContent = post.time || "";

    headerText.append(username, time);
    header.append(avatar, headerText);

    const content = document.createElement("div");
    content.className = "feed-content";
    content.textContent = post.content || "";

    card.append(header, content);

    if (images.length > 0) {
      const imageGrid = document.createElement("div");
      imageGrid.className = "feed-image-grid";

      images.forEach(img => {
        const image = document.createElement("img");
        image.src = img || "";
        image.alt = "post image";
        imageGrid.appendChild(image);
      });

      card.appendChild(imageGrid);
    }

    const footer = document.createElement("div");
    footer.className = "feed-footer";

    const likeButton = document.createElement("button");
    likeButton.className = "action-btn like-btn";
    likeButton.dataset.id = post.id;
    likeButton.type = "button";
    likeButton.setAttribute("aria-label", "Like post");
    likeButton.setAttribute("aria-pressed", "false");
    likeButton.append("❤️ ");

    const likeCount = document.createElement("span");
    likeCount.className = "like-count";
    likeCount.textContent = post.likes ?? 0;
    likeButton.appendChild(likeCount);

    const commentButton = document.createElement("button");
    commentButton.className = "action-btn comment-btn";
    commentButton.dataset.id = post.id;
    commentButton.type = "button";
    commentButton.setAttribute("aria-label", "Comment on post");
    commentButton.append("💬 ");

    const commentCount = document.createElement("span");
    commentCount.className = "comment-count";
    commentCount.textContent = post.comments ?? 0;
    commentButton.appendChild(commentCount);

    footer.append(likeButton, commentButton);
    card.appendChild(footer);

    /* Like button */
    likeButton.addEventListener("click", function () {
      const span = this.querySelector(".like-count");
      const post = allPosts.find(p => String(p.id) === String(this.dataset.id));
      if (!post) return;

      if (this.classList.contains("liked")) {
        this.classList.remove("liked");
        this.setAttribute("aria-pressed", "false");
        post.likes = Math.max(0, (post.likes ?? 1) - 1);
      } else {
        this.classList.add("liked");
        this.setAttribute("aria-pressed", "true");
        post.likes = (post.likes ?? 0) + 1;
      }
      span.textContent = post.likes;
    });

    /* Comment button */
    commentButton.addEventListener("click", function () {
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

let allPosts = [];
let currentSearch = "";
let currentTag = "All";

function formatTime(value) {
  if (!value) return "";

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;

  return date.toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric"
  });
}

function formatWeight(value) {
  if (value === null || value === undefined || value === "") return null;
  if (typeof value === "number") return `${value} kg`;
  return String(value);
}

function normalizePost(post) {
  const catchDetails = post.catchDetails || {};
  const location = catchDetails.location || {};
  const tags = Array.isArray(post.tags) ? post.tags : [];
  const category = post.category || (
    tags.includes("Gear") ? "Gear Review" :
    tags.includes("Question") ? "Question" :
    tags.length > 0 ? "Catch Report" :
    "General"
  );

  return {
    id: post.id,
    author: post.author || {
      userId: post.userId || "",
      username: post.username || "Unknown User",
      avatarUrl: post.avatar || ""
    },
    content: post.content || "",
    photos: Array.isArray(post.photos) ? post.photos : (Array.isArray(post.images) ? post.images : []),
    category,
    species: post.species ?? catchDetails.species ?? null,
    weightKg: post.weightKg ?? catchDetails.weight ?? null,
    bait: post.bait ?? catchDetails.bait ?? null,
    locationName: post.locationName ?? location.name ?? null,
    latitude: post.latitude ?? location.latitude ?? null,
    longitude: post.longitude ?? location.longitude ?? null,
    metrics: {
      likes: post.metrics?.likes ?? post.likes ?? 0,
      comments: post.metrics?.comments ?? post.metrics?.commentsCount ?? post.comments ?? 0
    },
    createdAt: post.createdAt || post.time || ""
  };
}

function loadPosts(path) {
  return fetch(path).then(res => {
    if (!res.ok) {
      throw new Error(`Failed to load mock posts: ${res.status}`);
    }
    return res.json();
  });
}

/* Load data: prefer database posts, then fall back to legacy mock JSON. */
loadPosts("/api/posts")
  .catch(err => {
    console.warn("Failed to load database posts, falling back to mock data:", err);
    return loadPosts("/api/feed-posts");
  })
  .then(jsonPosts => {
    const localPosts = JSON.parse(localStorage.getItem("userPosts") || "[]");
    allPosts = [...localPosts, ...jsonPosts].map(normalizePost);
    renderPosts(allPosts);
  })
  .catch(err => {
    console.error("Failed to load posts:", err);
    const localPosts = JSON.parse(localStorage.getItem("userPosts") || "[]");
    allPosts = localPosts.map(normalizePost);
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

    const images = Array.isArray(post.photos) ? post.photos : [];
    const author = post.author || {};
    const metrics = post.metrics || {};

    const header = document.createElement("div");
    header.className = "feed-header";

    const avatar = document.createElement("img");
    avatar.className = "feed-avatar";
    avatar.src = author.avatarUrl || "";
    avatar.alt = "avatar";

    const headerText = document.createElement("div");

    const username = document.createElement("div");
    username.className = "feed-username";
    username.textContent = author.username || "";

    const time = document.createElement("div");
    time.style.fontSize = "12px";
    time.style.color = "gray";
    time.textContent = formatTime(post.createdAt);

    headerText.append(username, time);
    header.append(avatar, headerText);

    const content = document.createElement("div");
    content.className = "feed-content";
    content.textContent = post.content || "";

    card.append(header, content);

    const details = [
      post.category,
      post.species,
      formatWeight(post.weightKg),
      post.bait ? `Bait: ${post.bait}` : null,
      post.locationName
    ].filter(Boolean);

    if (details.length > 0) {
      const meta = document.createElement("div");
      meta.className = "feed-meta";

      details.forEach(detail => {
        const item = document.createElement("span");
        item.textContent = detail;
        meta.appendChild(item);
      });

      card.appendChild(meta);
    }

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
    likeCount.textContent = metrics.likes ?? 0;
    likeButton.appendChild(likeCount);

    const commentButton = document.createElement("button");
    commentButton.className = "action-btn comment-btn";
    commentButton.dataset.id = post.id;
    commentButton.type = "button";
    commentButton.setAttribute("aria-label", "Comment on post");
    commentButton.append("💬 ");

    const commentCount = document.createElement("span");
    commentCount.className = "comment-count";
    commentCount.textContent = metrics.comments ?? 0;
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
        post.metrics.likes = Math.max(0, (post.metrics.likes ?? 1) - 1);
      } else {
        this.classList.add("liked");
        this.setAttribute("aria-pressed", "true");
        post.metrics.likes = (post.metrics.likes ?? 0) + 1;
      }
      span.textContent = post.metrics.likes;
    });

    /* Comment button */
    commentButton.addEventListener("click", function () {
      const input = prompt("Leave a comment:");
      if (input && input.trim()) {
        const span = this.querySelector(".comment-count");
        const post = allPosts.find(p => String(p.id) === String(this.dataset.id));
        if (!post) return;
        post.metrics.comments = (post.metrics.comments ?? 0) + 1;
        span.textContent = post.metrics.comments;
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
      post.category === currentTag
    );
  }

  if (currentSearch) {
    filtered = filtered.filter(post =>
      (post.content || "").toLowerCase().includes(currentSearch) ||
      (post.author?.username || "").toLowerCase().includes(currentSearch) ||
      (post.species || "").toLowerCase().includes(currentSearch) ||
      (post.locationName || "").toLowerCase().includes(currentSearch)
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

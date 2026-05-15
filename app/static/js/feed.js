let currentSearch = "";
let currentTag = "All";
let currentPage = 1;
let isLoading = false;

const feedContainer = document.getElementById("feedContainer");
const emptyMessage = document.querySelector(".feed-empty-message");
const loadMoreButton = document.getElementById("loadMorePosts");
const pageSize = Number(feedContainer?.dataset.pageSize || 10);
const searchInput = document.getElementById("searchInput");

function setLoading(isBusy) {
  isLoading = isBusy;
  if (loadMoreButton) {
    loadMoreButton.disabled = isBusy;
    loadMoreButton.textContent = isBusy ? "Loading..." : "Load more";
  }
}

function updateEmptyState(total) {
  if (emptyMessage) {
    emptyMessage.hidden = total !== 0;
  }
}

async function loadPosts({ reset = false } = {}) {
  if (!feedContainer || isLoading) return;

  const nextPage = reset ? 1 : currentPage + 1;
  const params = new URLSearchParams({
    page: String(nextPage),
    per_page: String(pageSize),
  });

  if (currentSearch) {
    params.set("q", currentSearch);
  }
  if (currentTag !== "All") {
    params.set("category", currentTag);
  }

  setLoading(true);
  if (reset) {
    feedContainer.querySelectorAll(".feed-post-item").forEach(item => {
      item.hidden = true;
    });
  }

  try {
    const response = await fetch(`/api/posts/feed?${params.toString()}`);
    if (!response.ok) {
      throw new Error("Failed to load posts");
    }

    const data = await response.json();
    feedContainer.insertAdjacentHTML("beforeend", data.html);

    currentPage = data.page;
    updateEmptyState(data.total);

    if (loadMoreButton) {
      loadMoreButton.hidden = !data.hasMore;
    }
  } catch (error) {
    console.error(error);
  } finally {
    setLoading(false);
  }
}

/* Search */
let searchTimer;
if (searchInput) {
  searchInput.addEventListener("input", () => {
    currentSearch = searchInput.value.trim();
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => loadPosts({ reset: true }), 250);
  });
}

/* Tag filter */
const tagsEl = document.querySelectorAll(".tag");
tagsEl.forEach(tag => {
  tag.addEventListener("click", () => {
    document.querySelector(".tag.active")?.classList.remove("active");
    tag.classList.add("active");
    currentTag = tag.innerText;
    loadPosts({ reset: true });
  });
});

if (loadMoreButton) {
  loadMoreButton.addEventListener("click", () => loadPosts());
}

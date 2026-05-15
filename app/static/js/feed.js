let currentSearch = "";
let currentTag = "All";
let currentPage = 1;
let isLoading = false;
let latestFetchId = 0;
let staleCleanupTimer;

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

function markCurrentPostsStale() {
  clearTimeout(staleCleanupTimer);
  feedContainer.querySelectorAll(".feed-post-item").forEach(item => {
    item.hidden = true;
    item.dataset.feedStale = "true";
  });
}

function cleanupStalePosts() {
  staleCleanupTimer = setTimeout(() => {
    feedContainer
      .querySelectorAll('.feed-post-item[data-feed-stale="true"]')
      .forEach(item => item.remove());
  }, 1000);
}

async function loadPosts({ reset = false } = {}) {
  if (!feedContainer) return;
  if (isLoading && !reset) return;

  const nextPage = reset ? 1 : currentPage + 1;
  const currentFetchId = ++latestFetchId;
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
    markCurrentPostsStale();
    feedContainer.style.opacity = "0.5";
  }

  try {
    const response = await fetch(`/api/posts/feed?${params.toString()}`);
    if (!response.ok) {
      throw new Error("Failed to load posts");
    }

    const data = await response.json();
    if (reset && currentFetchId !== latestFetchId) return;

    feedContainer.insertAdjacentHTML("beforeend", data.html);
    if (reset) {
      feedContainer.style.opacity = "1";
      cleanupStalePosts();
    }

    currentPage = data.page;
    updateEmptyState(data.total);

    if (loadMoreButton) {
      loadMoreButton.hidden = !data.hasMore;
    }
  } catch (error) {
    console.error(error);
  } finally {
    if (currentFetchId === latestFetchId) {
      setLoading(false);
      feedContainer.style.opacity = "1";
    }
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

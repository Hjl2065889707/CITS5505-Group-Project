let currentSearch = "";
let currentTag = "All";

/* Apply both filters together */
function applyFilters() {
  const postItems = document.querySelectorAll(".feed-post-item");
  const emptyMessage = document.querySelector(".feed-empty-message");
  let visibleCount = 0;

  postItems.forEach(item => {
    const matchesTag = currentTag === "All" || item.dataset.category === currentTag;
    const matchesSearch = !currentSearch || item.dataset.search.includes(currentSearch);
    const isVisible = matchesTag && matchesSearch;

    item.hidden = !isVisible;
    if (isVisible) visibleCount += 1;
  });

  if (emptyMessage) {
    emptyMessage.hidden = visibleCount !== 0;
  }
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

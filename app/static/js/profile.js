// Reload page when restored from browser back-forward cache (bfcache)
// so that follow state is always fresh from the server.
window.addEventListener("pageshow", (e) => {
  if (e.persisted) location.reload();
});

document.addEventListener("DOMContentLoaded", () => {
  // ── Tab switching ──
  const navTabs = document.querySelectorAll(".nav-tab");
  const tabContents = document.querySelectorAll(".tab-content");

  navTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      navTabs.forEach((t) => t.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));
      tab.classList.add("active");
      const targetId = tab.getAttribute("data-target");
      document.getElementById(targetId).classList.add("active");

      // Re-init carousels now that the hidden tab is visible
      if (typeof window.initAllCarousels === "function") {
        window.initAllCarousels();
      }
    });
  });

  // ── Follow button toggle ──
  const followBtn = document.querySelector(".follow-btn");
  if (followBtn) {
    const userId = followBtn.dataset.userId;

    // Hover effect: show "Unfollow" text when already following
    followBtn.addEventListener("mouseenter", () => {
      if (followBtn.classList.contains("following")) {
        followBtn.textContent = "Unfollow";
      }
    });
    followBtn.addEventListener("mouseleave", () => {
      if (followBtn.classList.contains("following")) {
        followBtn.textContent = "Following";
      }
    });

    followBtn.addEventListener("click", async () => {
      followBtn.disabled = true;
      try {
        const res = await fetch(`/api/users/${userId}/follow`, {
          method: "POST",
          headers: {
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
          },
        });
        if (!res.ok) throw new Error("Request failed");
        const data = await res.json();

        if (data.following) {
          followBtn.classList.add("following");
          followBtn.textContent = "Following";
        } else {
          followBtn.classList.remove("following");
          followBtn.textContent = "Follow";
        }

        // Update followers count on the page
        const countEl = document.getElementById("followersCount");
        if (countEl) countEl.textContent = data.followersCount;
      } catch (err) {
        console.error("Follow error:", err);
      } finally {
        followBtn.disabled = false;
      }
    });
  }

  // ── Followers / Following modal ──
  const modal = document.getElementById("followModal");
  const modalTitle = document.getElementById("followModalTitle");
  const modalList = document.getElementById("followModalList");
  const modalClose = document.getElementById("followModalClose");

  if (modal) {
    // Open modal when clicking followers/following stats
    document.querySelectorAll(".follow-stats a.stat").forEach((link) => {
      link.addEventListener("click", async (e) => {
        e.preventDefault();
        const listType = link.dataset.list; // "followers" or "following"
        const userId = link.dataset.userId;

        modalTitle.textContent =
          listType === "followers" ? "Followers" : "Following";
        modalList.innerHTML =
          '<p class="empty-state">Loading...</p>';
        modal.style.display = "flex";

        try {
          const res = await fetch(`/api/users/${userId}/${listType}`);
          if (!res.ok) throw new Error("Failed to load");
          const users = await res.json();

          if (users.length === 0) {
            modalList.innerHTML =
              '<p class="empty-state">No users to show.</p>';
            return;
          }

          modalList.innerHTML = "";
          users.forEach((u) => {
            const card = document.createElement("a");
            card.href = `/profile/${u.id}`;
            card.className = "follow-user-card";

            const img = document.createElement("img");
            img.src = u.avatarUrl;
            img.alt = u.username;

            const name = document.createElement("span");
            name.className = "follow-user-name";
            name.textContent = u.username; // textContent is XSS-safe

            card.appendChild(img);
            card.appendChild(name);
            modalList.appendChild(card);
          });
        } catch (err) {
          modalList.innerHTML =
            '<p class="empty-state">Failed to load list.</p>';
          console.error(err);
        }
      });
    });

    // Close modal
    modalClose.addEventListener("click", () => {
      modal.style.display = "none";
    });

    // Close on overlay click
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.style.display = "none";
    });

    // Close on Escape key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modal.style.display !== "none") {
        modal.style.display = "none";
      }
    });
  }

  // ── Decoupled Post Card Event Listener ──
  // Listen for custom events dispatched by the post-card component
  document.addEventListener("postSavedStateChanged", (e) => {
    const { isSaved } = e.detail;
    if (!isSaved) {
      // Find the card that triggered the event
      const postCard = e.target.closest(".post-card");
      if (!postCard) return;

      // Only animate and remove if the card is inside the "Saved Posts" tab
      const savedPostsTab = postCard.closest("#saved-posts");
      if (savedPostsTab) {
        postCard.style.transition = "opacity 0.3s ease, transform 0.3s ease";
        postCard.style.opacity = "0";
        postCard.style.transform = "scale(0.95)";
        setTimeout(() => {
          postCard.remove();
          // Show empty state if no posts left
          if (!savedPostsTab.querySelector(".post-card")) {
            savedPostsTab.innerHTML = '<p class="empty-state">No saved posts to show.</p>';
          }
        }, 300);
      }
    }
  });
});

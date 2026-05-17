/**
 * post-card.js — Interactive logic for the Post Card component.
 *
 * Uses Event Delegation: we listen on the document body to catch clicks
 * on any like/save button, even if the post card was loaded dynamically.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Event Delegation for action buttons
    document.body.addEventListener("click", handlePostCardClick);
    
    // Initialize carousels for any post cards currently on the page
    initAllCarousels();
  });
  
  /**
   * Handle clicks on Like or Save buttons inside any post card.
   */
  function handlePostCardClick(event) {
    const likeBtn = event.target.closest(".like-btn");
    const saveBtn = event.target.closest(".save-btn");
    const deleteBtn = event.target.closest(".delete-post-btn");
  
    if (likeBtn) {
      event.preventDefault(); // Prevent default if it happens to be a link
      toggleInteraction(likeBtn, "like");
    }
    
    if (saveBtn) {
      event.preventDefault();
      toggleInteraction(saveBtn, "save");
    }

    if (deleteBtn) {
      event.preventDefault();
      deletePost(deleteBtn);
    }
  }
  
  /**
   * Generic function to toggle an interaction (like or save) via the API.
   * @param {HTMLElement} button - The button element that was clicked.
   * @param {string} type - "like" or "save"
   */
  async function toggleInteraction(button, type) {
    const postId = button.dataset.postId;
    if (!postId) return;
  
    try {
      const response = await fetch(`/api/posts/${postId}/${type}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
        }
      });
  
      if (response.status === 401) {
        // Not logged in — redirect to login page
        window.location.href = "/login";
        return;
      }
  
      if (!response.ok) {
        console.error(`Failed to toggle ${type}`);
        return;
      }
  
      // Safety: if response is not JSON (e.g. HTML login redirect), go to login
      const contentType = response.headers.get("content-type") || "";
      if (!contentType.includes("application/json")) {
        window.location.href = "/login";
        return;
      }

      const data = await response.json();
      updateButtonUI(button, type, data);
  
    } catch (error) {
      console.error(`Error toggling ${type}:`, error);
    }
  }
  
  /**
   * Update the UI of the button based on the API response.
   */
  function updateButtonUI(button, type, data) {
    const icon = button.querySelector("i");
    const countSpan = button.querySelector(`.${type}-count`);
  
    if (type === "like") {
      const isLiked = data.liked;
      
      // Update icon classes
      if (isLiked) {
        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");
        button.classList.add("action-btn--active");
        button.setAttribute("aria-pressed", "true");
      } else {
        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");
        button.classList.remove("action-btn--active");
        button.setAttribute("aria-pressed", "false");
      }
  
      // Update count
      if (countSpan && data.likesCount !== undefined) {
        countSpan.textContent = data.likesCount;
      }
    } 
    else if (type === "save") {
      const isSaved = data.saved;
      
      if (isSaved) {
        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");
        button.classList.add("action-btn--active");
        button.setAttribute("aria-pressed", "true");
      } else {
        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");
        button.classList.remove("action-btn--active");
        button.setAttribute("aria-pressed", "false");
        
        // Dispatch a custom event so the parent page (e.g., profile.js) can handle list updates
        button.dispatchEvent(new CustomEvent("postSavedStateChanged", {
          bubbles: true,
          detail: { postId: button.dataset.postId, isSaved: false }
        }));
      }
    }
    // Notify parent pages, such as the map sidebar, that this post's interaction
    // state changed so they can refresh any cached post-card HTML.
    button.dispatchEvent(new CustomEvent("postInteractionChanged", {
      bubbles: true,
      detail: {
        type,
        postId: button.dataset.postId,
        ...data
      }
    }));
  }

  async function deletePost(button) {
    const postId = button.dataset.postId;
    if (!postId) return;
    if (!window.confirm("Delete this post?")) return;

    button.disabled = true;

    try {
      const response = await fetch(`/api/posts/${postId}`, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
        }
      });

      if (response.status === 401) {
        window.location.href = "/login";
        return;
      }

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        alert(data.error || "Failed to delete post.");
        return;
      }

      if (window.location.pathname === `/posts/${postId}`) {
        window.location.href = "/";
        return;
      }

      const postItem = button.closest(".feed-post-item") || button.closest(".post-card");
      postItem?.remove();
    } catch (error) {
      console.error("Error deleting post:", error);
      alert("Failed to delete post. Please try again.");
    } finally {
      button.disabled = false;
    }
  }
  
  /**
   * Carousel Initialization Logic
   * (Adapted from existing post.js to work on multiple carousels)
   */
  function initAllCarousels() {
    const carousels = document.querySelectorAll('.carousel-container');
    carousels.forEach(container => {
      initSingleCarousel(container);
    });
  }
  
  function initSingleCarousel(container) {
    const track = container.querySelector(".carousel-track");
    const slides = Array.from(track.querySelectorAll(".carousel-slide"));
    const nextBtn = container.querySelector(".next-btn");
    const prevBtn = container.querySelector(".prev-btn");
    const indicator = container.querySelector(".carousel-indicator");
  
    if (!track || slides.length <= 1) return; // No need for controls
  
    const updateUI = () => {
      const slideWidth = slides[0].getBoundingClientRect().width;

      // Guard: element is inside a hidden container (width = 0)
      if (slideWidth === 0) return;

      const currentIndex = Math.round(track.scrollLeft / slideWidth);
  
      if (indicator) {
        indicator.textContent = `${currentIndex + 1}/${slides.length}`;
      }
  
      if (prevBtn) {
        if (currentIndex === 0) prevBtn.classList.add('hidden');
        else prevBtn.classList.remove('hidden');
      }
  
      if (nextBtn) {
        if (currentIndex === slides.length - 1) nextBtn.classList.add('hidden');
        else nextBtn.classList.remove('hidden');
      }
    };
  
    track.addEventListener('scroll', () => {
      clearTimeout(track.scrollTimeout);
      track.scrollTimeout = setTimeout(updateUI, 50);
    });
  
    if (nextBtn) {
      nextBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent bubbling if card is clickable
        const slideWidth = slides[0].getBoundingClientRect().width;
        track.scrollBy({ left: slideWidth, behavior: 'smooth' });
      });
    }
  
    if (prevBtn) {
      prevBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const slideWidth = slides[0].getBoundingClientRect().width;
        track.scrollBy({ left: -slideWidth, behavior: 'smooth' });
      });
    }
  
    updateUI();
  }

  // Expose globally so other scripts (e.g. profile.js) can re-init
  // carousels after revealing hidden tabs.
  window.initAllCarousels = initAllCarousels;


/**
 * post.js — Logic specific to the Post Detail page.
 * 
 * Handles:
 *   - Comment submission (AJAX)
 *   - Comment deletion (AJAX, author-only)
 *
 * Note: Like, Save, and Carousel interactions are handled
 * globally by post-card.js using event delegation.
 */

document.addEventListener("DOMContentLoaded", () => {
  const commentForm = document.getElementById("comment-form");
  
  if (commentForm) {
    commentForm.addEventListener("submit", handleCommentSubmit);
  }

  // Event delegation for delete buttons (works for both server-rendered and AJAX-added comments)
  const commentList = document.getElementById("comment-list");
  if (commentList) {
    commentList.addEventListener("click", handleCommentListClick);
  }
});

// ── Comment Submission ───────────────────────────────────────────────

async function handleCommentSubmit(event) {
  event.preventDefault();
  
  const form = event.target;
  const postId = form.dataset.postId;
  const input = document.getElementById("comment-text");
  const submitBtn = form.querySelector(".comment-submit-btn");
  const text = input.value.trim();
  
  if (!text) return;
  
  // Disable form while submitting
  input.disabled = true;
  submitBtn.disabled = true;
  
  try {
    const response = await fetch(`/api/posts/${postId}/comments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ content: text })
    });
    
    if (response.status === 401) {
      window.location.href = "/login";
      return;
    }
    
    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.error || `Failed to post comment: ${response.statusText}`);
    }
    
    const newComment = await response.json();
    
    // Clear input
    input.value = "";
    
    // Dynamically insert the new comment into the DOM
    appendCommentToDOM(newComment);
    
    // Update comment count
    updateCommentCount(1);
    
  } catch (error) {
    console.error("Error submitting comment:", error);
    alert(error.message || "Failed to submit comment. Please try again.");
  } finally {
    // Re-enable form
    input.disabled = false;
    submitBtn.disabled = false;
    input.focus();
  }
}

function appendCommentToDOM(comment) {
  const commentList = document.getElementById("comment-list");
  const noCommentsMsg = document.getElementById("no-comments-msg");
  
  // Remove the "no comments yet" message if it exists
  if (noCommentsMsg) {
    noCommentsMsg.remove();
  }
  
  // The current user always owns their own new comment, so always show delete button
  const commentHTML = `
    <div class="comment-item" data-comment-id="${comment.id}" style="animation: fadeIn 0.3s ease;">
      <a href="/profile/${comment.userId || '#'}">
        <img src="${comment.avatarUrl}" alt="Avatar" class="comment-avatar" />
      </a>
      <div class="comment-body">
        <div class="comment-header">
          <div class="comment-header-left">
            <a href="/profile/${comment.userId || '#'}" class="comment-username">
              ${escapeHTML(comment.username)}
            </a>
            <span class="comment-time">Just now</span>
          </div>
          <button class="comment-delete-btn" data-comment-id="${comment.id}" data-post-id="${comment.postId || ''}" aria-label="Delete comment">
            <i class="fa-regular fa-trash-can"></i>
          </button>
        </div>
        <div class="comment-text">${escapeHTML(comment.content)}</div>
      </div>
    </div>
  `;
  
  // Insert at the top of the list
  commentList.insertAdjacentHTML("afterbegin", commentHTML);
  
  // Scroll to the comment
  window.scrollTo({
    top: document.querySelector('.comments-section').offsetTop - 60,
    behavior: 'smooth'
  });
}

// ── Comment Deletion ─────────────────────────────────────────────────

function handleCommentListClick(event) {
  const deleteBtn = event.target.closest(".comment-delete-btn");
  if (deleteBtn) {
    event.preventDefault();
    handleCommentDelete(deleteBtn);
  }
}

async function handleCommentDelete(button) {
  if (!confirm("Delete this comment?")) return;

  const commentId = button.dataset.commentId;
  // Get postId from the button or from the form
  const postId = button.dataset.postId || document.getElementById("comment-form")?.dataset.postId;

  if (!commentId || !postId) return;

  button.disabled = true;

  try {
    const response = await fetch(`/api/posts/${postId}/comments/${commentId}`, {
      method: "DELETE"
    });

    if (response.status === 403) {
      alert("You can only delete your own comments.");
      return;
    }

    if (!response.ok) {
      throw new Error("Failed to delete comment");
    }

    // Remove the comment from the DOM
    const commentItem = button.closest(".comment-item");
    if (commentItem) {
      commentItem.style.animation = "fadeIn 0.2s ease reverse";
      setTimeout(() => {
        commentItem.remove();
        updateCommentCount(-1);

        // Show "no comments" message if the list is now empty
        const commentList = document.getElementById("comment-list");
        if (commentList && commentList.children.length === 0) {
          commentList.innerHTML = '<p class="empty-state" id="no-comments-msg">No comments yet. Be the first to comment!</p>';
        }
      }, 200);
    }

  } catch (error) {
    console.error("Error deleting comment:", error);
    alert("Failed to delete comment. Please try again.");
  } finally {
    button.disabled = false;
  }
}

// ── Helpers ──────────────────────────────────────────────────────────

function updateCommentCount(delta) {
  const countDisplay = document.querySelector(".comment-count-display");
  if (countDisplay) {
    const currentCount = parseInt(countDisplay.textContent) || 0;
    countDisplay.textContent = Math.max(0, currentCount + delta);
  }
}

// Simple HTML escaper to prevent XSS if the user types HTML
function escapeHTML(str) {
  return str.replace(/[&<>'"]/g, 
    tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag)
  );
}

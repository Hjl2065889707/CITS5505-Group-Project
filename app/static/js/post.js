/**
 * post.js — Logic specific to the Post Detail page.
 * 
 * Note: Like, Save, and Carousel interactions are handled
 * globally by post-card.js using event delegation.
 */

document.addEventListener("DOMContentLoaded", () => {
  const commentForm = document.getElementById("comment-form");
  
  if (commentForm) {
    commentForm.addEventListener("submit", handleCommentSubmit);
  }
});

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
      throw new Error(`Failed to post comment: ${response.statusText}`);
    }
    
    const newComment = await response.json();
    
    // Clear input
    input.value = "";
    
    // Dynamically insert the new comment into the DOM
    appendCommentToDOM(newComment);
    
    // Update comment count
    updateCommentCount();
    
  } catch (error) {
    console.error("Error submitting comment:", error);
    alert("Failed to submit comment. Please try again.");
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
  
  // Build the HTML for the new comment
  // We use the same structure as in post_detail.html
  const commentHTML = `
    <div class="comment-item" style="animation: fadeIn 0.3s ease;">
      <a href="/profile/${comment.userId || '#'}">
        <img src="${comment.avatarUrl}" alt="Avatar" class="comment-avatar" />
      </a>
      <div class="comment-body">
        <div class="comment-header">
          <a href="/profile/${comment.userId || '#'}" class="comment-username">
            ${comment.username}
          </a>
          <span class="comment-time">Just now</span>
        </div>
        <div class="comment-text">${escapeHTML(comment.content)}</div>
      </div>
    </div>
  `;
  
  // Insert at the top of the list
  commentList.insertAdjacentHTML("afterbegin", commentHTML);
  
  // Scroll to the comment (optional, but good UX since input is fixed at bottom)
  window.scrollTo({
    top: document.querySelector('.comments-section').offsetTop - 60,
    behavior: 'smooth'
  });
}

function updateCommentCount() {
  const countDisplay = document.querySelector(".comment-count-display");
  if (countDisplay) {
    const currentCount = parseInt(countDisplay.textContent) || 0;
    countDisplay.textContent = currentCount + 1;
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

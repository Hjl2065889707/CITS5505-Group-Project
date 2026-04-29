let listenerAttached = false;

export function openSidebar(group, sidebar, closeSidebar) {
    group.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

    sidebar.innerHTML = `
    <div class="sidebar-header">
    <h2>Posts</h2>
    </div>

    <div class="sidebar-feed">
    ${group.map(post => renderPost(post)).join("")}
    </div>
    `;

    sidebar.classList.add("open");

    if (!listenerAttached) {
        sidebar.addEventListener("click", (e) => {

        // View Comments Button
        const btn = e.target.closest(".view-comments-btn");

        if (btn) {
        const comments = JSON.parse(btn.dataset.comments);

        const container = btn.parentElement;

        container.innerHTML = comments.map(comment => `
            <div class="comment-item">
            <span class="comment-username">${comment.username}</span>
            <span class="comment-text">${comment.text}</span>
            </div>
        `).join("");
        }

        // LIKE BUTTON
        const likeBtn = e.target.closest(".like-btn");

        if (likeBtn) {
        const countEl = likeBtn.querySelector(".like-count");
        const iconEl = likeBtn.querySelector(".like-icon");

        let count = Number(countEl.textContent);

        // Toggle like state
        if (likeBtn.classList.contains("liked")) {
            count--;
            likeBtn.classList.remove("liked");
            iconEl.textContent = "🤍";
        } else {
            count++;
            likeBtn.classList.add("liked");
            iconEl.textContent = "❤️";
        }

        countEl.textContent = count;
        }

    });

    listenerAttached = true;
    }
}

export function renderPost(post) {
  return `
    <article class="post-card">

      <div class="post-header">
        <img
          src="${post.author.avatarUrl}"
          alt="avatar"
          class="post-avatar"
        />

        <div class="post-user-info">
          <div class="post-username">${post.author.username}</div>
          <div class="post-time">${formatTime(post.createdAt)}</div>
        </div>
      </div>

      <div class="post-content">
        ${post.content}
      </div>

      ${
        post.photos?.length
          ? `
        <div class="carousel-container">
          <div class="carousel-track">
            ${post.photos
              .map(
                (photo) => `
              <div class="carousel-slide">
                <img src="${photo}" class="carousel-image" />
              </div>
            `
              )
              .join("")}
          </div>
        </div>
      `
          : ""
      }

      <div class="post-footer">
        <span 
            class="post-metric like-btn" 
            data-id="${post.id}"
        >
            <span class="like-icon">🤍</span>
            <span class="like-count">${post.metrics.likes}</span> Likes
        </span>

        <span class="post-metric">
            💬 ${post.metrics.commentsCount} Comments
        </span>
      </div>

      ${
        post.comments?.length
            ? `
        <div class="comments-preview">

            ${post.comments.slice(0, 2).map(comment => `
            <div class="comment-item">
                <span class="comment-username">${comment.username}</span>
                <span class="comment-text">${comment.text}</span>
            </div>
            `).join("")}

            ${
            post.comments.length > 2
                ? `<button 
                    class="view-comments-btn" 
                    data-comments='${JSON.stringify(post.comments)}'
                    >
                    View all comments
                    </button>`
                : ""
            }

        </div>
        `
            : ""
        }

    </article>
  `;
}

// Close sidebar
export function closeSidebar(sidebar) {
  sidebar.classList.remove("open");
}

export function showEmptySidebar(sidebar, closeSidebar) {
  sidebar.innerHTML = `
    <div class="sidebar-header">
      <h2>Welcome</h2>
    </div>

    <div class="sidebar-feed">
      <p style="padding: 10px; color: #666;">
        Get started: click on a marker to view posts.
      </p>
    </div>
  `;

  sidebar.classList.add("open");
}

export function formatTime(dateStr) {
  if (!dateStr) return "";

  const diff = (Date.now() - new Date(dateStr)) / 1000;

  if (diff < 3600) return Math.floor(diff / 60) + "m ago";
  if (diff < 86400) return Math.floor(diff / 3600) + "h ago";

  return "1d ago";
}

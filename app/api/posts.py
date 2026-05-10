"""Post-related API endpoints.

===== CRUD (Felix) =====
GET  /api/posts          — list posts (with ?category= and ?q= filters)
POST /api/posts          — create a new post (TODO)

===== Map (Chrommanito) =====
GET  /api/posts/map      — posts that have location data (TODO)

===== Legacy (temporary — remove after DB migration) =====
GET  /api/feed-posts     — mock feed data
GET  /api/my-posts       — mock user posts
GET  /api/saved-posts    — mock saved posts
"""

import json
from pathlib import Path

from flask import jsonify
from app import app, db
from app.models import Post, PostImage, Comment, PostLike, User

# ---------- Temporary mock-data paths (remove after DB migration) ----------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FEED_POSTS_FILE = BASE_DIR / "mockdata" / "feedPosts.json"


@app.route("/api/feed-posts")
def api_feed_posts():
    """Return feed posts as JSON for the frontend JS (legacy mock)."""
    with FEED_POSTS_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/api/my-posts")
def api_my_posts():
    """Return user's own posts as JSON (legacy mock)."""
    path = BASE_DIR / "mockdata" / "myPosts.json"
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/api/saved-posts")
def api_saved_posts():
    """Return user's saved posts as JSON (legacy mock)."""
    path = BASE_DIR / "mockdata" / "savedPosts.json"
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


# ===== CRUD (Felix) — TODO =============================================

# @app.route("/api/posts")
# def api_list_posts(): ...

# @app.route("/api/posts", methods=["POST"])
# @login_required
# def api_create_post(): ...


# ===== Map (Chrommanito) ========================================

@app.route("/api/posts/map")
def api_map_posts():
    """Return posts that have valid location data for the map page."""

    posts = (
        Post.query
        .filter(Post.latitude.isnot(None), Post.longitude.isnot(None))
        .order_by(Post.created_at.desc())
        .all()
    )

    result = []

    for post in posts:
        # Images
        post_images = (
            PostImage.query
            .filter_by(post_id=post.id)
            .order_by(PostImage.display_order.asc())
            .all()
        )
        photos = [image.image_url for image in post_images]

        # Comments
        post_comments = (
            Comment.query
            .filter_by(post_id=post.id)
            .order_by(Comment.created_at.asc())
            .all()
        )

        comments = []
        for comment in post_comments:
            comment_user = User.query.get(comment.user_id)

            comments.append({
                "id": str(comment.id),
                "username": comment_user.username if comment_user else "Unknown",
                "text": comment.content,
                "createdAt": comment.created_at.isoformat() if comment.created_at else "",
            })

        # Likes count
        likes_count = PostLike.query.filter_by(post_id=post.id).count()

        result.append({
            "id": str(post.id),
            "author": {
                "userId": str(post.user.id),
                "username": post.user.username,
                "avatarUrl": post.user.avatar_url or "/static/img/default-avatar.png",
            },
            "content": post.content,
            "photos": photos,
            "catchDetails": {
                "species": post.species or "",
                "weight": f"{post.weight_kg} kg" if post.weight_kg is not None else "",
                "bait": post.bait or "",
                "location": {
                    "name": post.location_name or "",
                    "latitude": post.latitude,
                    "longitude": post.longitude,
                },
            },
            "metrics": {
                "likes": likes_count,
                "commentsCount": len(comments),
            },
            "createdAt": post.created_at.isoformat() if post.created_at else "",
            "comments": comments,
        })

    return jsonify(result)

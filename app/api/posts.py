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
from app import app

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


# ===== Map (Chrommanito) — TODO ========================================

# @app.route("/api/posts/map")
# def api_map_posts(): ...

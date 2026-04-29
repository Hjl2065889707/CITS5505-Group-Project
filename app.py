import json
from pathlib import Path

from flask import Flask, render_template, abort, jsonify

app = Flask(__name__)

# ---------- Load mock data from JSON ----------

BASE_DIR = Path(__file__).resolve().parent
POSTS_FILE = BASE_DIR / "mockdata" / "myPosts.json"
FEED_POSTS_FILE = BASE_DIR / "mockdata" / "feedPosts.json"


def load_posts():
    """Read posts from the mock JSON file."""
    with POSTS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_post_by_id(post_id):
    """Find a single post by its id."""
    for post in load_posts():
        if post.get("id") == post_id:
            return post
    return None


# ---------- Routes ----------


@app.route("/")
def feed():
    """Home page — show all posts."""
    posts = load_posts()
    return render_template("feed.html", posts=posts, active_page="feed")


@app.route("/posts/<post_id>")
def post_detail(post_id):
    """Show a single post with its details."""
    post = get_post_by_id(post_id)
    if post is None:
        abort(404)
    return render_template("post_detail.html", post=post, active_page="feed")


@app.route("/create-post")
def create_post():
    """Show the create post form (static for now)."""
    return render_template("create_post.html", active_page="feed")


@app.route("/profile")
def profile():
    """Show user profile page."""
    return render_template("profile.html", active_page="profile")


@app.route("/settings")
def settings():
    """Show settings page."""
    return render_template("settings.html", active_page="profile")


@app.route("/map")
def map_page():
    """Show map page."""
    return render_template("map.html", active_page="map")


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page."""
    return render_template("404.html", active_page=""), 404


# ---------- API (JSON endpoints for JS) ----------


@app.route("/api/feed-posts")
def api_feed_posts():
    """Return feed posts as JSON for the frontend JS."""
    with FEED_POSTS_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/api/my-posts")
def api_my_posts():
    """Return user's own posts as JSON."""
    path = BASE_DIR / "mockdata" / "myPosts.json"
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/api/saved-posts")
def api_saved_posts():
    """Return user's saved posts as JSON."""
    path = BASE_DIR / "mockdata" / "savedPosts.json"
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


# ---------- Run ----------

if __name__ == "__main__":
    app.run(debug=True, port=5001)

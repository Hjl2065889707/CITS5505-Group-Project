"""Page routes — Feed, Create Post, Map.

Owner: Felix-Ma1209
"""

from flask import render_template
from app import app


@app.route("/")
def feed():
    """Home page — show all posts."""
    # TODO: replace mock data with Post.query (Sprint 1)
    return render_template("feed.html", active_page="feed")


@app.route("/create-post")
def create_post():
    """Show the create-post form (static for now)."""
    # TODO: pass CreatePostForm, handle POST (Sprint 1)
    return render_template("create_post.html", active_page="feed")


@app.route("/map")
def map_page():
    """Show the map page."""
    return render_template("map.html", active_page="map")

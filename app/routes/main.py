"""Page routes — Feed, Create Post, Map.

Owner: Felix-Ma1209
"""

from flask import render_template
from flask_login import login_required
from app import app
from app.models import Post


@app.route("/")
def feed():
    """Home page — show all posts."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("feed.html", posts=posts, active_page="feed")


@app.route("/create-post")
@login_required
def create_post():
    """Show the create-post form."""
    return render_template("create_post.html", active_page="feed")


@app.route("/map")
def map_page():
    """Show the map page."""
    return render_template("map.html", active_page="map")

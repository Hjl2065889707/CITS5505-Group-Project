"""Page routes — Feed, Create Post, Map.

Owner: Felix-Ma1209
"""

from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Post

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def feed():
    """Home page — show all posts."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("feed.html", posts=posts, active_page="feed")


@main_bp.route("/create-post")
@login_required
def create_post():
    """Show the create-post form."""
    return render_template("create_post.html", active_page="feed")


@main_bp.route("/map")
def map_page():
    """Show the map page."""
    return render_template("map.html", active_page="map")

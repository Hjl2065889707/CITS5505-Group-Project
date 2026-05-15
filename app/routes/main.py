"""Page routes — Feed, Create Post, Map.

Owner: Felix-Ma1209
"""

from flask import Blueprint, render_template
from flask_login import login_required
from app.api.posts import FEED_PAGE_SIZE, build_posts_query

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def feed():
    """Home page — show the first page of posts."""
    page = build_posts_query().paginate(
        page=1,
        per_page=FEED_PAGE_SIZE,
        error_out=False,
    )
    return render_template(
        "feed.html",
        posts=page.items,
        has_more_posts=page.has_next,
        feed_page_size=FEED_PAGE_SIZE,
        active_page="feed",
    )


@main_bp.route("/create-post")
@login_required
def create_post():
    """Show the create-post form."""
    return render_template("create_post.html", active_page="feed")


@main_bp.route("/map")
def map_page():
    """Show the map page."""
    return render_template("map.html", active_page="map")

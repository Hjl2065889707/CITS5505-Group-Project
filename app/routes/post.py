"""Post detail route.

Owner: Hjl2065889707
"""

from flask import Blueprint, render_template, abort
from app import db
from app.models import Post, Comment

post_bp = Blueprint("post", __name__)


@post_bp.route("/posts/<int:post_id>")
def post_detail(post_id):
    """Show a single post with its details and comments."""
    # Find the post by ID, return 404 if not found or soft-deleted
    post = db.session.get(Post, post_id)
    if not post or post.is_deleted:
        abort(404)

    # Query all comments for this post, newest first
    comments = (
        Comment.query
        .filter_by(post_id=post_id)
        .order_by(Comment.created_at.desc())
        .all()
    )

    # Send post and comments data to the template for server-side rendering
    return render_template(
        "post_detail.html", 
        post=post, 
        comments=comments, 
        active_page="feed"
    )

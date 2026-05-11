"""Profile & Settings routes.

Owner: Hjl2065889707
"""

from flask import render_template, abort
from flask_login import current_user, login_required
from app import app, db
from app.models import User, Post, SavedPost


@app.route("/profile")
@app.route("/profile/<int:user_id>")
def profile(user_id=None):
    """Show a user's profile page. If user_id is None, show current user."""
    # Determine who we are viewing
    if user_id is not None:
        target_user = db.session.get(User, user_id)
    elif current_user.is_authenticated:
        target_user = current_user
    else:
        # Not logged in and no user_id specified → redirect to login
        from flask import redirect, url_for
        return redirect(url_for('login'))

    if not target_user:
        abort(404)

    my_posts = (
        Post.query.filter_by(user_id=target_user.id)
        .order_by(Post.created_at.desc())
        .all()
    )

    saved_post_ids = [sp.post_id for sp in SavedPost.query.filter_by(user_id=target_user.id).all()]
    saved_posts = Post.query.filter(Post.id.in_(saved_post_ids)).all() if saved_post_ids else []

    # Follow stats
    is_following = False
    if current_user.is_authenticated and current_user.id != target_user.id:
        is_following = current_user.is_following(target_user)

    return render_template("profile.html",
                           user=target_user,
                           my_posts=my_posts,
                           saved_posts=saved_posts,
                           is_following=is_following,
                           followers_count=target_user.followers_count(),
                           following_count=target_user.following_count(),
                           active_page="profile")


@app.route("/settings")
@login_required
def settings():
    """Show settings page for the current user."""
    return render_template("settings.html", user=current_user, active_page="profile")


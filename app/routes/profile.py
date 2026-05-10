"""Profile & Settings routes.

Owner: Hjl2065889707
"""

from flask import render_template, abort
from app import app, db
from app.models import User, Post, SavedPost


@app.route("/profile")
@app.route("/profile/<int:user_id>")
def profile(user_id=None):
    """Show a user's profile page. If user_id is None, show current user."""
    # TODO: Replace with current_user once Oliver finishes Auth. 
    # For now, we mock the current user as the seeded 'demo_user' (ID 1)
    current_user = db.session.get(User, 1)
    
    target_user_id = user_id if user_id is not None else (current_user.id if current_user else 1)
    target_user = db.session.get(User, target_user_id)
    
    if not target_user:
        abort(404)
        
    my_posts = (
        Post.query.filter_by(user_id=target_user.id)
        .order_by(Post.created_at.desc())
        .all()
    )
    
    saved_post_ids = [sp.post_id for sp in SavedPost.query.filter_by(user_id=target_user.id).all()]
    saved_posts = Post.query.filter(Post.id.in_(saved_post_ids)).all() if saved_post_ids else []

    return render_template("profile.html", 
                           user=target_user,
                           current_user=current_user,
                           my_posts=my_posts,
                           saved_posts=saved_posts,
                           active_page="profile")

@app.route("/settings")
def settings():
    """Show settings page for the current user."""
    # TODO: Replace with @login_required + current_user once Auth is integrated
    user = db.session.get(User, 1)
    if not user:
        abort(404)
    return render_template("settings.html", user=user, active_page="profile")

"""Profile & Settings routes.

Owner: Hjl2065889707
"""

from flask import render_template, abort
from app import app, db
from app.models import User, Post, SavedPost


@app.route("/profile")
def profile():
    """Show current user's profile page."""
    # TODO: Replace with current_user once Oliver finishes Auth. 
    # For now, we mock the current user as the seeded 'demo_user' (ID 1)
    current_user = db.session.get(User, 1)
    if not current_user:
        abort(404)
        
    my_posts = (
        Post.query.filter_by(user_id=current_user.id)
        .order_by(Post.created_at.desc())
        .all()
    )
    
    saved_post_ids = [sp.post_id for sp in SavedPost.query.filter_by(user_id=current_user.id).all()]
    saved_posts = Post.query.filter(Post.id.in_(saved_post_ids)).all() if saved_post_ids else []

    return render_template("profile.html", 
                           user=current_user,
                           my_posts=my_posts,
                           saved_posts=saved_posts,
                           active_page="profile")

@app.route("/settings")
def settings():
    """Show settings page."""
    # TODO: pass SettingsForm, handle POST to save changes
    return render_template("settings.html", active_page="profile")

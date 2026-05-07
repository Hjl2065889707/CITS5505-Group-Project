"""Interaction API endpoints — Like, Save, Comment.

Owner: Hjl2065889707
"""

from flask import jsonify, request, abort
from flask_login import current_user
from app import app, db
from app.models import Post, PostLike, SavedPost, Comment, User

def _get_current_user_id():
    """Temporary helper to get current user ID, falling back to 1 (demo_user) if unauthenticated."""
    if current_user and current_user.is_authenticated:
        return current_user.id
    return 1

@app.route("/api/posts/<int:post_id>/like", methods=["POST"])
def toggle_like(post_id):
    user_id = _get_current_user_id()
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
        
    existing_like = PostLike.query.filter_by(user_id=user_id, post_id=post_id).first()
    
    if existing_like:
        db.session.delete(existing_like)
        liked = False
    else:
        new_like = PostLike(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        liked = True
        
    db.session.commit()
    
    like_count = PostLike.query.filter_by(post_id=post_id).count()
    return jsonify({"liked": liked, "likesCount": like_count})


@app.route("/api/posts/<int:post_id>/save", methods=["POST"])
def toggle_save(post_id):
    user_id = _get_current_user_id()
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
        
    existing_save = SavedPost.query.filter_by(user_id=user_id, post_id=post_id).first()
    
    if existing_save:
        db.session.delete(existing_save)
        saved = False
    else:
        new_save = SavedPost(user_id=user_id, post_id=post_id)
        db.session.add(new_save)
        saved = True
        
    db.session.commit()
    return jsonify({"saved": saved})


@app.route("/api/posts/<int:post_id>/comments", methods=["POST"])
def add_comment(post_id):
    user_id = _get_current_user_id()
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
        
    data = request.get_json()
    if not data or not data.get("content"):
        return jsonify({"error": "Content is required"}), 400
        
    content = data.get("content").strip()
    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400
        
    comment = Comment(user_id=user_id, post_id=post_id, content=content)
    db.session.add(comment)
    db.session.commit()
    
    # Fetch user details for the response
    user = db.session.get(User, user_id)
    
    return jsonify({
        "id": comment.id,
        "content": comment.content,
        "createdAt": comment.created_at.isoformat(),
        "userId": user.id,
        "username": user.username,
        "avatarUrl": user.avatar_url or "/static/img/default-avatar.png"
    }), 201

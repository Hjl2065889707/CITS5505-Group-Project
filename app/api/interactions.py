"""Interaction API endpoints — Like, Save, Comment.

Owner: Hjl2065889707

Security notes:
  - All endpoints validate resource existence (404 if not found).
  - Comment content is type-checked and length-limited server-side.
  - Authentication: currently falls back to demo_user (ID 1) because
    the Auth module is not yet integrated. Once Auth is merged,
    replace _get_current_user_id() with @login_required decorator.
  - CSRF: will be enforced globally via Flask-WTF CSRFProtect once
    the Auth branch is merged. See __init__.py TODO.
"""

from flask import jsonify, request, abort
from flask_login import current_user
from app import app, db
from app.models import Post, PostLike, SavedPost, Comment, User

# --- Constants ---
MAX_COMMENT_LENGTH = 2000  # Server-enforced max characters per comment


def _get_current_user_id():
    """Return the current user's ID.

    Falls back to 1 (demo_user) while Auth is not yet integrated.
    TODO: Replace with @login_required once Auth branch is merged.
    """
    if current_user and current_user.is_authenticated:
        return current_user.id
    return 1


# ── Like ──────────────────────────────────────────────────────────────

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


# ── Save ──────────────────────────────────────────────────────────────

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


# ── Comment (Create) ──────────────────────────────────────────────────

@app.route("/api/posts/<int:post_id>/comments", methods=["POST"])
def add_comment(post_id):
    user_id = _get_current_user_id()
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)

    # --- Zero-trust input validation ---
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    content = data.get("content")

    # Type check: content must be a string (reject lists, dicts, numbers)
    if not isinstance(content, str):
        return jsonify({"error": "Content must be a string"}), 400

    content = content.strip()
    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400

    if len(content) > MAX_COMMENT_LENGTH:
        return jsonify({
            "error": f"Comment too long. Maximum {MAX_COMMENT_LENGTH} characters."
        }), 400

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


# ── Comment (Delete) ─────────────────────────────────────────────────

@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(post_id, comment_id):
    user_id = _get_current_user_id()

    comment = db.session.get(Comment, comment_id)
    if not comment or comment.post_id != post_id:
        abort(404)

    # Authorization: only the comment author can delete their own comment
    if comment.user_id != user_id:
        return jsonify({"error": "You can only delete your own comments"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"deleted": True, "commentId": comment_id})

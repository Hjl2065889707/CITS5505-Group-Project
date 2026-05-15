"""Interaction API endpoints — Like, Save, Comment.

Owner: Hjl2065889707

Security notes:
  - All endpoints require authentication via @login_required.
  - All endpoints validate resource existence (404 if not found).
  - Comment content is type-checked and length-limited server-side.
"""

from flask import Blueprint, jsonify, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Post, PostLike, SavedPost, Comment

api_interactions_bp = Blueprint("api_interactions", __name__)

# --- Constants ---
MAX_COMMENT_LENGTH = 2000  # Server-enforced max characters per comment


# ── Like ──────────────────────────────────────────────────────────────

@api_interactions_bp.route("/posts/<int:post_id>/like", methods=["POST"])
@login_required
def toggle_like(post_id):
    post = db.session.get(Post, post_id)
    if not post or post.is_deleted:
        abort(404)

    existing_like = PostLike.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if existing_like:
        db.session.delete(existing_like)
        liked = False
    else:
        new_like = PostLike(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        liked = True

    db.session.commit()

    like_count = PostLike.query.filter_by(post_id=post_id).count()
    return jsonify({"liked": liked, "likesCount": like_count})


# ── Save ──────────────────────────────────────────────────────────────

@api_interactions_bp.route("/posts/<int:post_id>/save", methods=["POST"])
@login_required
def toggle_save(post_id):
    post = db.session.get(Post, post_id)
    if not post or post.is_deleted:
        abort(404)

    existing_save = SavedPost.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if existing_save:
        db.session.delete(existing_save)
        saved = False
    else:
        new_save = SavedPost(user_id=current_user.id, post_id=post_id)
        db.session.add(new_save)
        saved = True

    db.session.commit()
    return jsonify({"saved": saved})


# ── Comment (Create) ──────────────────────────────────────────────────

@api_interactions_bp.route("/posts/<int:post_id>/comments", methods=["POST"])
@login_required
def add_comment(post_id):
    post = db.session.get(Post, post_id)
    if not post or post.is_deleted:
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

    comment = Comment(user_id=current_user.id, post_id=post_id, content=content)
    db.session.add(comment)
    db.session.commit()

    return jsonify({
        "id": comment.id,
        "content": comment.content,
        "createdAt": comment.created_at.isoformat(),
        "userId": current_user.id,
        "username": current_user.username,
        "avatarUrl": current_user.avatar_url or "/static/img/default-avatar.png"
    }), 201


# ── Comment (Delete) ─────────────────────────────────────────────────

@api_interactions_bp.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=["DELETE"])
@login_required
def delete_comment(post_id, comment_id):
    post = db.session.get(Post, post_id)
    if not post or post.is_deleted:
        abort(404)

    comment = db.session.get(Comment, comment_id)
    if not comment or comment.post_id != post_id:
        abort(404)

    # Authorization: only the comment author can delete their own comment
    if comment.user_id != current_user.id:
        return jsonify({"error": "You can only delete your own comments"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"deleted": True, "commentId": comment_id})

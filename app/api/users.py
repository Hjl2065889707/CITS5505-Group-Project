"""User-related API endpoints — Profile update, Avatar upload, Password change.

Owner: Hjl2065889707

Security notes:
  - All endpoints validate input server-side (zero-trust).
  - Avatar files are saved locally with secure_filename().
  - Password change requires the current password to be verified first.
  - Authentication: falls back to demo_user (ID 1) until Auth is integrated.
"""

import os
import time

from flask import jsonify, request, abort, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from sqlalchemy import func
from app import app, db
from app.models import User

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5 MB


def _get_current_user():
    """Return the current user object.
    Falls back to demo_user (ID 1) while Auth is not yet integrated.
    TODO: Replace with @login_required once Auth branch is merged.
    """
    if current_user and current_user.is_authenticated:
        return current_user
    return db.session.get(User, 1)


def _allowed_image(filename):
    """Check if the filename has an allowed image extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


# ── Update Profile ────────────────────────────────────────────────────

@app.route("/api/users/me", methods=["PUT"])
def update_profile():
    """Update the current user's username and/or bio."""
    user = _get_current_user()
    if not user:
        abort(401)

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    errors = {}

    # --- Username validation ---
    if "username" in data:
        username = data["username"]
        if not isinstance(username, str):
            errors["username"] = "Username must be a string"
        else:
            username = username.strip()
            if len(username) < 3 or len(username) > 50:
                errors["username"] = "Username must be 3-50 characters"
            else:
                # Check uniqueness (case-insensitive, exclude self)
                existing = User.query.filter(
                    func.lower(User.username) == username.lower(),
                    User.id != user.id
                ).first()
                if existing:
                    errors["username"] = "This username is already taken"
                else:
                    user.username = username

    # --- Bio validation ---
    if "bio" in data:
        bio = data["bio"]
        if not isinstance(bio, str):
            errors["bio"] = "Bio must be a string"
        else:
            bio = bio.strip()
            if len(bio) > 500:
                errors["bio"] = "Bio must be under 500 characters"
            else:
                user.bio = bio

    if errors:
        return jsonify({"error": errors}), 400

    db.session.commit()

    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "bio": user.bio,
            "avatarUrl": user.avatar_url or "/static/img/default-avatar.png"
        }
    })


# ── Upload Avatar ─────────────────────────────────────────────────────

@app.route("/api/users/me/avatar", methods=["POST"])
def upload_avatar():
    """Upload and update the current user's avatar image."""
    user = _get_current_user()
    if not user:
        abort(401)

    if 'avatar' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['avatar']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not _allowed_image(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: PNG, JPG, JPEG, WebP"}), 400

    # Check file size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > MAX_AVATAR_SIZE:
        return jsonify({"error": "File too large. Maximum 5MB"}), 400

    # Build safe filename: <user_id>_<timestamp>.<ext>
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename(f"{user.id}_{int(time.time())}.{ext}")

    # Ensure upload directory exists
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    # Update user record
    user.avatar_url = f"/static/uploads/avatars/{filename}"
    db.session.commit()

    return jsonify({
        "success": True,
        "avatarUrl": user.avatar_url
    })


# ── Change Password ───────────────────────────────────────────────────

@app.route("/api/users/me/password", methods=["PUT"])
def change_password():
    """Change the current user's password."""
    user = _get_current_user()
    if not user:
        abort(401)

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")

    # Type checks
    if not isinstance(current_password, str) or not isinstance(new_password, str):
        return jsonify({"error": "Passwords must be strings"}), 400

    # Verify current password
    if not user.check_password(current_password):
        return jsonify({"error": "Current password is incorrect"}), 400

    # Validate new password
    new_password = new_password.strip()
    if len(new_password) < 6:
        return jsonify({"error": "New password must be at least 6 characters"}), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"success": True})

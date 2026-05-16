"""Post-related API endpoints.

===== CRUD (Felix) =====
GET  /api/posts          — list posts (with ?category= and ?q= filters)
POST /api/posts          — create a new post

===== Map (Chrommanito) =====
GET  /api/posts/map      — posts that have location data
"""

import base64
import re
import uuid
from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    render_template_string,
    request,
)
from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db
from app.models import Post, PostImage, User

api_posts_bp = Blueprint("api_posts", __name__)

ALLOWED_CATEGORIES = {"Catch Report", "Gear Review", "Question", "General"}
FEED_PAGE_SIZE = 10
DATA_URL_RE = re.compile(r"^data:image/(png|jpe?g|gif|webp);base64,(.+)$", re.I)
MAX_INLINE_IMAGE_BYTES = 2 * 1024 * 1024


def _clean_optional_text(value, max_length):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Optional text fields must be strings.")
    value = value.strip()
    if not value:
        return None
    if len(value) > max_length:
        raise ValueError(f"Text field cannot exceed {max_length} characters.")
    return value


def _clean_optional_float(value, field_name):
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a number.") from exc


def _store_image_url_or_data_url(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Each photo must be a non-empty string.")

    value = value.strip()
    match = DATA_URL_RE.match(value)
    if not match:
        if len(value) > 255:
            raise ValueError("Photo URL is too long.")
        return value

    extension = "jpg" if match.group(1).lower() in {"jpg", "jpeg"} else match.group(1).lower()
    try:
        image_bytes = base64.b64decode(match.group(2), validate=True)
    except ValueError as exc:
        raise ValueError("Photo data is not valid base64.") from exc

    if len(image_bytes) > MAX_INLINE_IMAGE_BYTES:
        raise ValueError("Each uploaded image must be under 2 MB.")

    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = f"post-{uuid.uuid4().hex}.{extension}"
    (upload_dir / filename).write_bytes(image_bytes)
    return f"/static/uploads/{filename}"


def _serialize_post(post):
    images = sorted(post.images, key=lambda image: image.display_order or 0)

    return {
        "id": post.id,
        "author": {
            "userId": post.user.id if post.user else None,
            "username": post.user.username if post.user else "Unknown User",
            "avatarUrl": post.user.avatar_url if post.user else None,
        },
        "content": post.content,
        "photos": [image.image_url for image in images],
        "category": post.category,
        "species": post.species,
        "weightKg": post.weight_kg,
        "bait": post.bait,
        "locationName": post.location_name,
        "latitude": post.latitude,
        "longitude": post.longitude,
        "metrics": {
            "likes": len(post.likes),
            "comments": len(post.comments),
        },
        "createdAt": post.created_at.isoformat() if post.created_at else None,
        "isDeleted": post.is_deleted,
    }


def build_posts_query(category=None, search=None):
    """Build the shared Feed/API post query with optional filters."""
    search = (search or "").strip()
    query = Post.query.filter(Post.is_deleted.is_(False))

    if category and category != "All":
        query = query.filter(Post.category == category)

    if search:
        pattern = f"%{search}%"
        query = query.join(User).filter(
            or_(
                Post.content.ilike(pattern),
                Post.species.ilike(pattern),
                Post.location_name.ilike(pattern),
                User.username.ilike(pattern),
            )
        )

    return query.order_by(Post.created_at.desc())


# ===== CRUD (Felix) =====================================================


@api_posts_bp.route("/posts")
def api_list_posts():
    """Return database posts in the unified Feed/Create Post JSON shape."""
    category = request.args.get("category")
    search = request.args.get("q")

    posts = build_posts_query(category=category, search=search).all()
    return jsonify([_serialize_post(post) for post in posts])


@api_posts_bp.route("/posts/feed")
def api_feed_posts():
    """Return one page of Feed post HTML for incremental loading."""
    category = request.args.get("category")
    search = request.args.get("q")
    page_number = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", FEED_PAGE_SIZE, type=int)

    page_number = max(page_number, 1)
    per_page = min(max(per_page, 1), 25)

    page = build_posts_query(category=category, search=search).paginate(
        page=page_number,
        per_page=per_page,
        error_out=False,
    )
    html = "".join(
        render_template("components/_feed_post_item.html", post=post)
        for post in page.items
    )

    return jsonify(
        {
            "html": html,
            "page": page.page,
            "hasMore": page.has_next,
            "total": page.total,
        }
    )


@api_posts_bp.route("/posts", methods=["POST"])
def api_create_post():
    """Create a post from the Create Post page."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    content = data.get("content")
    if not isinstance(content, str) or not content.strip():
        return jsonify({"error": "Content is required."}), 400

    category = data.get("category")
    if category not in ALLOWED_CATEGORIES:
        return jsonify({"error": "Please select a valid category."}), 400

    if not current_user.is_authenticated:
        return jsonify({"error": "Please log in before creating a post."}), 401

    try:
        weight_kg = _clean_optional_float(data.get("weightKg"), "weightKg")
        if weight_kg is not None and weight_kg < 0:
            return jsonify({"error": "weightKg cannot be negative."}), 400

        latitude = _clean_optional_float(data.get("latitude"), "latitude")
        longitude = _clean_optional_float(data.get("longitude"), "longitude")

        post = Post(
            user_id=current_user.id,
            content=content.strip(),
            category=category,
            species=_clean_optional_text(data.get("species"), 120),
            weight_kg=weight_kg,
            bait=_clean_optional_text(data.get("bait"), 120),
            location_name=_clean_optional_text(data.get("locationName"), 120),
            latitude=latitude,
            longitude=longitude,
        )

        photos = data.get("photos") or []
        if not isinstance(photos, list):
            return jsonify({"error": "photos must be an array."}), 400
        if len(photos) > 8:
            return jsonify({"error": "You can upload up to 8 photos."}), 400

        image_urls = [_store_image_url_or_data_url(photo) for photo in photos]
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    db.session.add(post)
    db.session.flush()

    for index, image_url in enumerate(image_urls):
        db.session.add(PostImage(
            post_id=post.id,
            image_url=image_url,
            display_order=index,
        ))

    db.session.commit()

    return jsonify(_serialize_post(post)), 201


@api_posts_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@login_required
def api_delete_post(post_id):
    """Soft-delete a post owned by the current user."""
    post = db.session.get(Post, post_id)
    if not post or post.is_deleted:
        return jsonify({"error": "Post not found."}), 404

    if post.user_id != current_user.id:
        return jsonify({"error": "You can only delete your own posts."}), 403

    post.is_deleted = True
    db.session.commit()

    return jsonify({"deleted": True, "postId": post_id})



# ===== Map (Chrommanito) ========================================

@api_posts_bp.route("/posts/map")
def api_map_posts():
    """Return posts that have valid location data for the map page."""

    posts = (
        Post.query
        .filter(
            Post.is_deleted.is_(False),
            Post.latitude.isnot(None),
            Post.longitude.isnot(None),
        )
        .order_by(Post.created_at.desc())
        .all()
    )

    macro_template = """
    {% from 'components/_post_card.html' import post_card %}
    {{ post_card(post, variant='compact') }}
    """

    result = []

    for post in posts:
        html_string = render_template_string(macro_template, post=post)

        result.append({
            "id": str(post.id),
            "latitude": post.latitude,
            "longitude": post.longitude,
            "html": html_string,
        })

    return jsonify(result)

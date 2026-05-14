"""API sub-package — Blueprints are registered in create_app()."""


# ---------------------------------------------------------------------------
# Shared serialiser — used by every API module to keep the JSON shape
# consistent across Feed, Profile, and Map.
# ---------------------------------------------------------------------------

def serialize_post(post, current_user=None):
    """Convert a Post ORM object to a JSON-ready dict.

    This is the **single source of truth** for the post JSON format.
    Feed, Profile, Map and all API endpoints must use this function.
    """
    from app.models import PostImage  # lazy import to avoid circular

    images = sorted(post.images, key=lambda img: img.display_order)

    location = None
    if post.latitude is not None:
        location = {
            "name": post.location_name,
            "latitude": post.latitude,
            "longitude": post.longitude,
        }

    return {
        "id": post.id,
        "author": {
            "id": post.user.id,
            "username": post.user.username,
            "avatarUrl": post.user.avatar_url or "/static/img/default-avatar.png",
        },
        "content": post.content,
        "images": [img.image_url for img in images],
        "catchDetails": {
            "species": post.species,
            "weight": post.weight_kg,
            "bait": post.bait,
            "location": location,
        },
        "category": post.category,
        "metrics": {
            "likes": len(post.likes),
            "commentsCount": len(post.comments),
            "isLiked": (
                any(l.user_id == current_user.id for l in post.likes)
                if current_user
                else False
            ),
            "isSaved": (
                any(s.user_id == current_user.id for s in post.saved_by)
                if current_user
                else False
            ),
        },
        "createdAt": post.created_at.isoformat() if post.created_at else None,
    }

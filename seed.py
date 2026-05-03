import json
import re
from datetime import datetime
from pathlib import Path
from werkzeug.security import generate_password_hash
from app import app

from models import db, User, Post, PostImage, Comment, PostLike, SavedPost


BASE_DIR = Path(__file__).resolve().parent
POSTS_FILE = BASE_DIR / "mockdata" / "myPosts.json"


def parse_date(value: str | None) -> datetime | None:
    """Parse an ISO 8601 string into a timezone-aware datetime."""
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_weight(value: str | None) -> float | None:
    """
    Parse a weight string from JSON into a float (kg).
    Handles values like "2.5", "2.5kg", "2.5 kg", etc.
    Returns None if the value is missing or unparseable.
    """
    if not value:
        return None
    match = re.search(r"\d+(?:\.\d+)?", str(value))
    return float(match.group()) if match else None


with app.app_context():
    db.drop_all()
    db.create_all()

    demo_user = User(
        username="demo_user",
        email="demo@example.com",
        password_hash=generate_password_hash("password123"),
        avatar_url="",
        bio="Demo user for seeded posts.",
    )

    db.session.add(demo_user)
    db.session.commit()

    with POSTS_FILE.open("r", encoding="utf-8") as f:
        posts_data = json.load(f)

    for post_data in posts_data:
        catch_details = post_data.get("catchDetails", {})
        location = catch_details.get("location", {})

        post = Post(
            user_id=demo_user.id,
            content=post_data.get("content", ""),
            location_name=location.get("name"),
            latitude=location.get("latitude"),
            longitude=location.get("longitude"),
            species=catch_details.get("species"),
            weight_kg=parse_weight(catch_details.get("weight")),
            bait=catch_details.get("bait"),
            category=post_data.get("category"),
            created_at=parse_date(post_data.get("createdAt")),
        )

        db.session.add(post)
        db.session.flush()

        for index, image_url in enumerate(post_data.get("photos", [])):
            db.session.add(PostImage(
                post_id=post.id,
                image_url=image_url,
                display_order=index,
            ))

        db.session.add(PostLike(
            user_id=demo_user.id,
            post_id=post.id,
        ))

        db.session.add(Comment(
            user_id=demo_user.id,
            post_id=post.id,
            content="Nice catch!",
        ))

        db.session.add(SavedPost(
            user_id=demo_user.id,
            post_id=post.id,
        ))
        
    db.session.commit()
    print(f"Seeded {len(posts_data)} posts for user '{demo_user.username}'.")
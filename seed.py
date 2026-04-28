import json
from datetime import datetime
from pathlib import Path
from werkzeug.security import generate_password_hash

# This script depends on SQLAlchemy models being added to app.py:
# db, User, Post, PostImage, Comment, Like, SavedPost
from app import app, db, User, Post, PostImage, Comment


BASE_DIR = Path(__file__).resolve().parent

# Load posts from the JSON file in the mockdata directory
POSTS_FILE = BASE_DIR / "mockdata" / ""


# Helper function to parse ISO 8601 date strings, handling 'Z' for UTC
def parse_date(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


with app.app_context():
    # Clear existing data and create tables
    # db.drop_all()
    db.create_all()

    # placeholder user for all seeded posts
    demo_user = User(
        username="demo_user",
        email="demo@example.com",
        password_hash=generate_password_hash("password123"),
        avatar_url="",
        bio="Demo user for seeded posts."
    )

    db.session.add(demo_user)
    db.session.commit()

    with POSTS_FILE.open("r", encoding="utf-8") as file:
        posts_data = json.load(file)

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
            weight=catch_details.get("weight"),
            bait=catch_details.get("bait"),
            category=post_data.get("category"),
            created_at=parse_date(post_data.get("createdAt")),
        )

        db.session.add(post)
        db.session.flush()

        # Creates image table
        for index, image_url in enumerate(post_data.get("photos", [])):
            image = PostImage(
                post_id=post.id,
                image_url=image_url,
                display_order=index
            )
            db.session.add(image)

        # --- FUTURE: Seed likes ---
        # like = Like(
        #     user_id=demo_user.id,
        #     post_id=post.id
        # )
        # db.session.add(like)

        # --- FUTURE: Seed comments ---
        # for post in posts:
        #     comment = Comment(
        #         user_id=demo_user.id,
        #         post_id=post.id,
        #         text="Nice catch!"
        #     )
        #     db.session.add(comment)

    db.session.commit()

    print(f"Seeded {len(posts_data)} posts.")
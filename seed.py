"""Seed the database with demo data for development and marking.

Creates 5 demo users, 10+ posts covering every category, interactions
(likes, comments, saves, follows), and 3 distinct fishing locations with
map-visible coordinates.

Usage:
    flask db upgrade   # apply migrations first
    python seed.py     # then seed
"""

from datetime import datetime, timedelta, timezone

from app import create_app, db
from app.models import (
    Comment,
    Follow,
    Post,
    PostImage,
    PostLike,
    SavedPost,
    User,
)

app = create_app()


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

USERS = [
    {
        "username": "BassHunter",
        "email": "basshunter@example.com",
        "password": "password123",
        "bio": "Weekend angler from Perth. Love freshwater bass fishing.",
        "avatar_url": "https://images.unsplash.com/photo-1527980965255-d3b416303d12?w=200",
    },
    {
        "username": "OceanExplorer",
        "email": "ocean@example.com",
        "password": "password123",
        "bio": "Deep-sea fishing enthusiast. Chasing tuna and marlin.",
        "avatar_url": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200",
    },
    {
        "username": "ReelQueen",
        "email": "reelqueen@example.com",
        "password": "password123",
        "bio": "Fly fishing addict. Catch and release only.",
        "avatar_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200",
    },
    {
        "username": "TroutMaster",
        "email": "trout@example.com",
        "password": "password123",
        "bio": "Mountain streams and trout — that's my life.",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200",
    },
    {
        "username": "CastAway",
        "email": "castaway@example.com",
        "password": "password123",
        "bio": "New to fishing. Learning every day!",
        "avatar_url": "https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?w=200",
    },
]

# Base time: posts spread over the last 2 weeks
_BASE = datetime(2026, 5, 3, 8, 0, 0, tzinfo=timezone.utc)

POSTS = [
    # --- Catch Report (4 posts, 3 with locations) ---
    {
        "user_idx": 0,
        "content": (
            "Great weekend out on Swan River! The weather was perfect and the "
            "fish were biting early in the morning. Best catch of the season."
        ),
        "category": "Catch Report",
        "species": "Largemouth Bass",
        "weight_kg": 2.04,
        "bait": "Plastic Worm",
        "location_name": "Swan River, Perth",
        "latitude": -31.9505,
        "longitude": 115.8605,
        "photos": [
            "https://images.pexels.com/photos/3220790/pexels-photo-3220790.jpeg?w=800",
        ],
        "offset_days": 0,
    },
    {
        "user_idx": 1,
        "content": (
            "First time deep-sea fishing and it did not disappoint. Fought this "
            "beauty for 20 minutes before bringing it on board."
        ),
        "category": "Catch Report",
        "species": "Yellowfin Tuna",
        "weight_kg": 32.0,
        "bait": "Live Bait",
        "location_name": "Fremantle Coast",
        "latitude": -32.0569,
        "longitude": 115.7439,
        "photos": [
            "https://images.pexels.com/photos/2131967/pexels-photo-2131967.jpeg?w=800",
            "https://images.pexels.com/photos/2132007/pexels-photo-2132007.jpeg?w=800",
        ],
        "offset_days": 1,
    },
    {
        "user_idx": 2,
        "content": (
            "Caught a beautiful rainbow trout on a dry fly this morning at "
            "Canning River. The colours were incredible."
        ),
        "category": "Catch Report",
        "species": "Rainbow Trout",
        "weight_kg": 1.8,
        "bait": "Dry Fly",
        "location_name": "Canning River, Perth",
        "latitude": -32.0140,
        "longitude": 115.9440,
        "photos": [
            "https://images.pexels.com/photos/1630343/pexels-photo-1630343.jpeg?w=800",
        ],
        "offset_days": 3,
    },
    {
        "user_idx": 3,
        "content": (
            "Unexpected barramundi catch while shore fishing at dawn. "
            "Released it safely after a quick photo."
        ),
        "category": "Catch Report",
        "species": "Barramundi",
        "weight_kg": 5.6,
        "bait": "Soft Plastic",
        "location_name": None,
        "latitude": None,
        "longitude": None,
        "photos": [
            "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg?w=800",
        ],
        "offset_days": 5,
    },
    # --- Gear Review (3 posts) ---
    {
        "user_idx": 0,
        "content": (
            "Just upgraded to the Shimano Stella SW 8000. Incredible smoothness "
            "and drag power. Worth every penny for offshore work."
        ),
        "category": "Gear Review",
        "species": None,
        "weight_kg": None,
        "bait": None,
        "location_name": None,
        "latitude": None,
        "longitude": None,
        "photos": [
            "https://images.pexels.com/photos/1291712/pexels-photo-1291712.jpeg?w=800",
        ],
        "offset_days": 2,
    },
    {
        "user_idx": 4,
        "content": (
            "Picked up a budget telescopic rod for kayak fishing. Surprisingly "
            "sturdy for the price. Great for beginners who are just getting started."
        ),
        "category": "Gear Review",
        "species": None,
        "weight_kg": None,
        "bait": None,
        "location_name": None,
        "latitude": None,
        "longitude": None,
        "photos": [
            "https://images.pexels.com/photos/1076429/pexels-photo-1076429.jpeg?w=800",
        ],
        "offset_days": 7,
    },
    {
        "user_idx": 2,
        "content": (
            "New waders review: Patagonia Swiftcurrent. Waterproof, breathable, "
            "and the built-in gravel guards are a game changer for river fishing."
        ),
        "category": "Gear Review",
        "species": None,
        "weight_kg": None,
        "bait": None,
        "location_name": None,
        "latitude": None,
        "longitude": None,
        "photos": [
            "https://images.pexels.com/photos/1755243/pexels-photo-1755243.jpeg?w=800",
        ],
        "offset_days": 9,
    },
    # --- Question (2 posts) ---
    {
        "user_idx": 4,
        "content": (
            "What's the best time of day to fish for bream in Perth estuaries? "
            "I've been going at midday but having no luck. Any tips?"
        ),
        "category": "Question",
        "species": "Bream",
        "weight_kg": None,
        "bait": None,
        "location_name": None,
        "latitude": None,
        "longitude": None,
        "photos": [],
        "offset_days": 4,
    },
    {
        "user_idx": 3,
        "content": (
            "Can anyone recommend a good braided line for light tackle estuary "
            "fishing? Looking for something under $30 that doesn't tangle easily."
        ),
        "category": "Question",
        "species": None,
        "weight_kg": None,
        "bait": None,
        "location_name": None,
        "latitude": None,
        "longitude": None,
        "photos": [],
        "offset_days": 6,
    },
    # --- General (2 posts) ---
    {
        "user_idx": 1,
        "content": (
            "Nothing beats a sunrise on the water. Even when the fish aren't "
            "biting, mornings like this make it all worthwhile."
        ),
        "category": "General",
        "species": None,
        "weight_kg": None,
        "bait": None,
        "location_name": "Swan River, Perth",
        "latitude": -31.9505,
        "longitude": 115.8605,
        "photos": [
            "https://images.pexels.com/photos/1574843/pexels-photo-1574843.jpeg?w=800",
        ],
        "offset_days": 8,
    },
    {
        "user_idx": 4,
        "content": (
            "Just joined CatchLog! Excited to learn from the community and "
            "share my beginner fishing adventures. Tight lines everyone!"
        ),
        "category": "General",
        "species": None,
        "weight_kg": None,
        "bait": None,
        "location_name": None,
        "latitude": None,
        "longitude": None,
        "photos": [],
        "offset_days": 10,
    },
]


# Pre-written comments so different users interact with each other
COMMENTS = [
    # (commenter_user_idx, post_idx, comment_text)
    (1, 0, "That's a solid bass! What pound test line were you using?"),
    (2, 0, "Swan River never disappoints. Nice one!"),
    (0, 1, "32 kg tuna is insane! What boat were you on?"),
    (3, 1, "Dream catch right there. Congrats!"),
    (4, 2, "Beautiful colours on that trout. Catch and release?"),
    (0, 2, "Canning River is underrated. Great spot."),
    (1, 4, "Shimano Stella is the GOAT. Best reel I've ever owned."),
    (4, 7, "Try dawn or dusk — bream are most active at low light."),
    (2, 7, "Use fresh prawns as bait, works every time in the estuary."),
    (3, 9, "Welcome to the community! Feel free to ask anything."),
]


# ---------------------------------------------------------------------------
# Seed
# ---------------------------------------------------------------------------

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables recreated.")

    # ── Create users ──
    users = []
    for u in USERS:
        user = User(
            username=u["username"],
            email=u["email"],
            bio=u["bio"],
            avatar_url=u["avatar_url"],
        )
        user.set_password(u["password"])
        db.session.add(user)
        users.append(user)

    db.session.flush()  # assign IDs
    print(f"Created {len(users)} users.")

    # ── Create posts ──
    posts = []
    for p in POSTS:
        post = Post(
            user_id=users[p["user_idx"]].id,
            content=p["content"],
            category=p["category"],
            species=p["species"],
            weight_kg=p["weight_kg"],
            bait=p["bait"],
            location_name=p["location_name"],
            latitude=p["latitude"],
            longitude=p["longitude"],
            created_at=_BASE + timedelta(days=p["offset_days"]),
        )
        db.session.add(post)
        db.session.flush()

        for idx, photo_url in enumerate(p["photos"]):
            db.session.add(PostImage(
                post_id=post.id,
                image_url=photo_url,
                display_order=idx,
            ))

        posts.append(post)

    print(f"Created {len(posts)} posts (4 Catch Report, 3 Gear Review, 2 Question, 2 General).")

    # ── Add comments ──
    for commenter_idx, post_idx, text in COMMENTS:
        db.session.add(Comment(
            user_id=users[commenter_idx].id,
            post_id=posts[post_idx].id,
            content=text,
        ))
    print(f"Added {len(COMMENTS)} comments.")

    # ── Add likes (spread across users and posts) ──
    like_pairs = [
        (0, 1), (0, 2), (0, 9),
        (1, 0), (1, 2), (1, 4),
        (2, 0), (2, 1), (2, 3),
        (3, 0), (3, 1), (3, 5),
        (4, 0), (4, 1), (4, 2), (4, 4), (4, 9),
    ]
    for user_idx, post_idx in like_pairs:
        db.session.add(PostLike(
            user_id=users[user_idx].id,
            post_id=posts[post_idx].id,
        ))
    print(f"Added {len(like_pairs)} likes.")

    # ── Add saved posts ──
    save_pairs = [
        (0, 1), (0, 4),
        (1, 0), (1, 2),
        (2, 3), (2, 5),
        (4, 0), (4, 1), (4, 4),
    ]
    for user_idx, post_idx in save_pairs:
        db.session.add(SavedPost(
            user_id=users[user_idx].id,
            post_id=posts[post_idx].id,
        ))
    print(f"Added {len(save_pairs)} saved posts.")

    # ── Add follows ──
    follow_pairs = [
        (0, 1), (0, 2),
        (1, 0), (1, 2),
        (2, 0), (2, 3),
        (3, 2),
        (4, 0), (4, 1), (4, 2), (4, 3),
    ]
    for follower_idx, followed_idx in follow_pairs:
        db.session.add(Follow(
            follower_id=users[follower_idx].id,
            followed_id=users[followed_idx].id,
        ))
    print(f"Added {len(follow_pairs)} follow relationships.")

    db.session.commit()
    print("\nSeed complete! Log in with any user (password: password123).")
    print("Users:", ", ".join(u["username"] for u in USERS))

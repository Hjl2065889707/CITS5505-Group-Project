from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def utcnow():
    """Timezone-aware UTC timestamp for use as a column default."""
    return datetime.now(timezone.utc)


# =====================
# User
# =====================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    avatar_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    # Relationships
    posts = db.relationship("Post", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)
    likes = db.relationship("PostLike", backref="user", lazy=True)
    saved_posts = db.relationship("SavedPost", backref="user", lazy=True)


# =====================
# Post
# =====================
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    content = db.Column(db.Text, nullable=False)

    # Location
    location_name = db.Column(db.String(120), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Fishing details
    species = db.Column(db.String(120), nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)
    bait = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    # Relationships
    images = db.relationship(
        "PostImage",
        backref="post",
        lazy=True,
        cascade="all, delete-orphan",
    )
    comments = db.relationship(
        "Comment",
        backref="post",
        lazy=True,
        cascade="all, delete-orphan",
    )
    likes = db.relationship(
        "PostLike",
        backref="post",
        lazy=True,
        cascade="all, delete-orphan",
    )
    saved_by = db.relationship(
        "SavedPost",
        backref="post",
        lazy=True,
        cascade="all, delete-orphan",
    )


# =====================
# PostImage
# =====================
class PostImage(db.Model):
    __tablename__ = "post_images"

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    display_order = db.Column(db.Integer, default=0)


# =====================
# Comment
# =====================
class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)


# =====================
# PostLike (many-to-many join table)
# =====================
class PostLike(db.Model):
    __tablename__ = "post_likes"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)

    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)


# =====================
# SavedPost (many-to-many join table)
# =====================
class SavedPost(db.Model):
    __tablename__ = "saved_posts"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)

    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)
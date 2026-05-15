"""Database models (M in MVC)."""

from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


def utcnow():
    """Timezone-aware UTC timestamp for use as a column default."""
    return datetime.now(timezone.utc)


# =====================
# User
# =====================
class User(UserMixin, db.Model):
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

    # Follow relationships (self-referential many-to-many via Follow table)
    following = db.relationship(
        "Follow", foreign_keys="Follow.follower_id",
        backref=db.backref("follower", lazy="joined"), lazy="dynamic"
    )
    followers = db.relationship(
        "Follow", foreign_keys="Follow.followed_id",
        backref=db.backref("followed", lazy="joined"), lazy="dynamic"
    )

    # ── Password helpers ──

    def set_password(self, password):
        """Hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a plaintext password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    # ── Follow helpers ──

    def is_following(self, user):
        """Check if this user is following the given user."""
        return self.following.filter_by(followed_id=user.id).first() is not None

    def followers_count(self):
        """Return the number of followers."""
        return self.followers.count()

    def following_count(self):
        """Return the number of users this user is following."""
        return self.following.count()


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

    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

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


# =====================
# Follow (user-to-user relationship)
# =====================
class Follow(db.Model):
    __tablename__ = "follows"

    follower_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True
    )
    followed_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True
    )

    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

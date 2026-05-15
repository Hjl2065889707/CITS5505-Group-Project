"""Unit tests for Profile & Interaction features.

Owner: Hjl2065889707

Covers:
  - Like toggle (POST /api/posts/<id>/like)
  - Save toggle (POST /api/posts/<id>/save)
  - Add comment (POST /api/posts/<id>/comments)
  - Delete own comment (DELETE /api/posts/<id>/comments/<id>)
  - Cannot delete another user's comment (403)
  - Follow toggle (POST /api/users/<id>/follow)
"""

import pytest

from app import create_app, db
from app.models import User, Post
from config import TestConfig


@pytest.fixture()
def app():
    """Create a test application with an in-memory database."""
    test_app = create_app(TestConfig)

    # 'with test_app.app_context():' pushes the Flask application context.
    with test_app.app_context():
        db.create_all()

        # Create two users for interaction tests
        tester = User(username="tester", email="tester@example.com")
        tester.set_password("password123")

        other = User(username="other_user", email="other@example.com")
        other.set_password("password123")

        db.session.add_all([tester, other])
        db.session.flush()

        # Create a post owned by tester (will have id=1)
        post = Post(
            user_id=tester.id,
            content="Test post for interactions",
            category="General",
        )
        db.session.add(post)
        db.session.commit()

    # pauses this fixture and hands 'test_app' over to the test function.
    # Once the test finishes, code execution resumes right below this yield statement.
    yield test_app

    # Cleanup phase. It runs AFTER the test finishes.
    # Open the context to clean up the database.
    with test_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Flask test client — maintains session cookies between requests."""
    return app.test_client()


def login_as(client, username="tester"):
    """Helper: log in as the given user via the login form."""
    client.post(
        "/login",
        data={"username_or_email": username, "password": "password123"},
        follow_redirects=True,
    )


# ── Test 1: Like toggle ──────────────────────────────────────────────


def test_like_toggle(client):
    """Liking a post twice should like then unlike it."""
    login_as(client)

    # First request → like
    r1 = client.post("/api/posts/1/like")
    data1 = r1.get_json()
    assert data1["liked"] is True
    assert data1["likesCount"] == 1

    # Second request → unlike
    r2 = client.post("/api/posts/1/like")
    data2 = r2.get_json()
    assert data2["liked"] is False
    assert data2["likesCount"] == 0


# ── Test 2: Save toggle ──────────────────────────────────────────────


def test_save_toggle(client):
    """Saving a post twice should save then unsave it."""
    login_as(client)

    r1 = client.post("/api/posts/1/save")
    assert r1.get_json()["saved"] is True

    r2 = client.post("/api/posts/1/save")
    assert r2.get_json()["saved"] is False


# ── Test 3: Add comment ──────────────────────────────────────────────


def test_add_comment(client):
    """A logged-in user should be able to post a comment."""
    login_as(client)

    r = client.post("/api/posts/1/comments", json={"content": "Great catch!"})

    assert r.status_code == 201
    data = r.get_json()
    assert data["content"] == "Great catch!"
    assert data["username"] == "tester"


# ── Test 4: Delete own comment ────────────────────────────────────────


def test_delete_own_comment(client):
    """A user should be able to delete their own comment."""
    login_as(client)

    # Create a comment first
    r1 = client.post("/api/posts/1/comments", json={"content": "To be deleted"})
    comment_id = r1.get_json()["id"]

    # Delete it
    r2 = client.delete(f"/api/posts/1/comments/{comment_id}")
    assert r2.get_json()["deleted"] is True


# ── Test 5: Cannot delete another user's comment ─────────────────────


def test_cannot_delete_others_comment(client):
    """Deleting someone else's comment should return 403 Forbidden."""
    # other_user creates a comment
    login_as(client, "other_user")
    r1 = client.post("/api/posts/1/comments", json={"content": "Other's comment"})
    comment_id = r1.get_json()["id"]

    # Log out and log back in as tester
    client.post("/logout", follow_redirects=True)
    login_as(client, "tester")

    # Try to delete other_user's comment → should fail
    r2 = client.delete(f"/api/posts/1/comments/{comment_id}")
    assert r2.status_code == 403


# ── Test 6: Follow toggle ────────────────────────────────────────────


def test_follow_toggle(client):
    """Following a user twice should follow then unfollow them."""
    login_as(client)

    # Follow other_user (id=2)
    r1 = client.post("/api/users/2/follow")
    data1 = r1.get_json()
    assert data1["following"] is True
    assert data1["followersCount"] == 1

    # Unfollow
    r2 = client.post("/api/users/2/follow")
    data2 = r2.get_json()
    assert data2["following"] is False
    assert data2["followersCount"] == 0

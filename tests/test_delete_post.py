import pytest

from app import create_app, db
from app.models import Post, User
from config import TestConfig


@pytest.fixture()
def app():
    test_app = create_app(TestConfig)

    with test_app.app_context():
        db.create_all()

        owner = User(username="owner", email="owner@example.com")
        owner.set_password("password123")
        other = User(username="other", email="other@example.com")
        other.set_password("password123")
        db.session.add_all([owner, other])
        db.session.flush()

        db.session.add_all([
            Post(
                user_id=owner.id,
                content="Owner post to delete",
                category="General",
                latitude=-31.95,
                longitude=115.86,
            ),
            Post(
                user_id=other.id,
                content="Other visible post",
                category="Catch Report",
            ),
        ])
        db.session.commit()

    yield test_app

    with test_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def login_as(client, username):
    return client.post(
        "/login",
        data={"username_or_email": username, "password": "password123"},
        follow_redirects=True,
    )


def test_guest_cannot_delete_post(client):
    response = client.delete("/api/posts/1")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Authentication required"


def test_non_author_cannot_delete_post(client):
    login_as(client, "other")

    response = client.delete("/api/posts/1")

    assert response.status_code == 403
    assert response.get_json()["error"] == "You can only delete your own posts."


def test_author_soft_delete_hides_post_from_public_surfaces(client, app):
    login_as(client, "owner")

    response = client.delete("/api/posts/1")

    assert response.status_code == 200
    assert response.get_json() == {"deleted": True, "postId": 1}

    with app.app_context():
        post = db.session.get(Post, 1)
        assert post.is_deleted is True

    feed_response = client.get("/")
    assert b"Owner post to delete" not in feed_response.data
    assert b"Other visible post" in feed_response.data

    feed_api_response = client.get("/api/posts/feed")
    assert "Owner post to delete" not in feed_api_response.get_json()["html"]

    posts_api_response = client.get("/api/posts")
    assert "Owner post to delete" not in [
        post["content"] for post in posts_api_response.get_json()
    ]

    map_response = client.get("/api/posts/map")
    assert map_response.get_json() == []

    detail_response = client.get("/posts/1")
    assert detail_response.status_code == 404


def test_delete_button_only_shows_for_post_author(client):
    login_as(client, "owner")

    owner_view = client.get("/")
    assert b'data-post-id="1" aria-label="Delete post"' in owner_view.data
    assert b'data-post-id="2" aria-label="Delete post"' not in owner_view.data

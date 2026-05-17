import pytest

from app import create_app, db
from app.models import Post, User
from config import TestConfig


@pytest.fixture()
def app():
    test_app = create_app(TestConfig)

    with test_app.app_context():
        db.create_all()

        user = User(username="maptester", email="maptester@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        located_post = Post(
            user_id=user.id,
            content="Visible map post",
            category="Catch Report",
            species="Bream",
            location_name="Swan River",
            latitude=-31.9523,
            longitude=115.8613,
        )

        no_location_post = Post(
            user_id=user.id,
            content="Post without coordinates",
            category="General",
            latitude=None,
            longitude=None,
        )

        deleted_location_post = Post(
            user_id=user.id,
            content="Deleted map post",
            category="Catch Report",
            latitude=-31.95,
            longitude=115.86,
            is_deleted=True,
        )

        db.session.add_all([
            located_post,
            no_location_post,
            deleted_location_post,
        ])
        db.session.commit()

    yield test_app

    with test_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_map_api_returns_200(client):
    response = client.get("/api/posts/map")

    assert response.status_code == 200


def test_map_api_returns_only_posts_with_location_data(client):
    response = client.get("/api/posts/map")

    assert response.status_code == 200

    data = response.get_json()
    contents = [post["html"] for post in data]

    assert len(data) == 1
    assert "Visible map post" in contents[0]
    assert "Post without coordinates" not in contents[0]
    assert "Deleted map post" not in contents[0]


def test_map_api_response_contains_required_map_fields(client):
    response = client.get("/api/posts/map")

    assert response.status_code == 200

    data = response.get_json()
    post = data[0]

    assert "id" in post
    assert "latitude" in post
    assert "longitude" in post
    assert "html" in post

    assert post["latitude"] == -31.9523
    assert post["longitude"] == 115.8613
    assert isinstance(post["html"], str)
    assert len(post["html"]) > 0
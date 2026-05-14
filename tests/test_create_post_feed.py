import pytest

from app import create_app, db
from app.models import Post, User
from config import TestConfig


class CreatePostFeedTestConfig(TestConfig):
    UPLOAD_FOLDER = "/tmp/catchlog-test-uploads"


@pytest.fixture()
def app():
    test_app = create_app(CreatePostFeedTestConfig)

    with test_app.app_context():
        db.create_all()
        user = User(username="tester", email="tester@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    yield test_app

    with test_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client):
    return client.post(
        "/login",
        data={
            "username_or_email": "tester",
            "password": "password123",
        },
        follow_redirects=True,
    )


def test_guest_cannot_create_post(client):
    response = client.post(
        "/api/posts",
        json={
            "content": "Guest post should fail",
            "category": "General",
            "photos": [],
        },
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Please log in before creating a post."


def test_empty_content_returns_400(client):
    login(client)

    response = client.post(
        "/api/posts",
        json={
            "content": "",
            "category": "General",
            "photos": [],
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Content is required."


def test_invalid_category_returns_400(client):
    login(client)

    response = client.post(
        "/api/posts",
        json={
            "content": "Caught a nice fish today.",
            "category": "Bass",
            "photos": [],
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Please select a valid category."


def test_logged_in_user_can_create_post(client, app):
    login(client)

    response = client.post(
        "/api/posts",
        json={
            "content": "Created from pytest",
            "category": "Catch Report",
            "species": "Trout",
            "weightKg": 1.5,
            "bait": "Fly",
            "locationName": "Swan River",
            "latitude": -31.95,
            "longitude": 115.86,
            "photos": [],
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["content"] == "Created from pytest"
    assert data["category"] == "Catch Report"
    assert data["species"] == "Trout"
    assert data["weightKg"] == 1.5
    assert data["locationName"] == "Swan River"
    assert data["latitude"] == -31.95
    assert data["longitude"] == 115.86

    with app.app_context():
        post = Post.query.filter_by(content="Created from pytest").one()
        assert post.user.username == "tester"


def test_feed_route_returns_200(client):
    response = client.get("/")

    assert response.status_code == 200


def test_feed_renders_database_posts(client, app):
    with app.app_context():
        user = User.query.filter_by(username="tester").one()
        post = Post(
            user_id=user.id,
            content="Feed visible pytest post",
            category="General",
            species="Bream",
            location_name="Canning River",
        )
        db.session.add(post)
        db.session.commit()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Feed visible pytest post" in response.data
    assert b"Bream" in response.data
    assert b"Canning River" in response.data

import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))
os.makedirs(os.path.join(basedir, "instance"), exist_ok=True)


class Config:
    """Application configuration — reads secrets from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "instance", "catchlog.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload

    @staticmethod
    def init_app(app):
        if not app.config.get("SECRET_KEY"):
            raise RuntimeError("SECRET_KEY environment variable must be set.")


class TestConfig(Config):
    """Overrides for pytest — uses in-memory SQLite."""

    SECRET_KEY = "test-secret-key"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

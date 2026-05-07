"""Import all route sub-modules so their @app.route decorators register."""

from app.routes import main, auth, post, profile  # noqa: F401

"""
CatchLog — Flask application package.

Uses the Application Factory pattern (create_app) so that different
configurations can be passed for development, testing, etc.
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# ---------------------------------------------------------------------------
# Extension instances (created here so route / model files can import them)
# ---------------------------------------------------------------------------
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_class=None):
    """Application factory — create and configure the Flask app."""
    if config_class is None:
        from config import Config
        config_class = Config

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialise extensions with this app instance
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Redirect target when @login_required fails
    login_manager.login_view = "login"

    # ── Flask-Login callbacks ──

    @login_manager.user_loader
    def load_user(user_id):
        """Flask-Login callback — load user from session cookie."""
        from app.models import User
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        """Return JSON 401 for API requests, redirect to login for page requests."""
        if request.path.startswith("/api/"):
            return jsonify({"error": "Authentication required"}), 401
        return redirect(url_for("login"))

    # ── Error handlers ──

    @app.errorhandler(404)
    def page_not_found(_error):
        return render_template("404.html", active_page=""), 404

    return app


# ---------------------------------------------------------------------------
# Module-level app instance for backward compatibility.
# Route files still use `from app import app` + `@app.route(...)`.
# This will be removed after Blueprint migration (Step 2).
# ---------------------------------------------------------------------------
app = create_app()

# Import routes & models at the bottom so their @app.route decorators register.
from app.routes import main, auth, post, profile  # noqa: E402, F401
from app.api import posts, interactions, users     # noqa: E402, F401
from app import models                             # noqa: E402, F401

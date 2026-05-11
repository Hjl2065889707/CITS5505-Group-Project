"""
CatchLog — Flask application package.

Initialises the Flask app, database, login manager, and migration engine.
Route and model imports are placed at the **bottom** to avoid circular
dependencies, following the recommended Flask package pattern.
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# ---------------------------------------------------------------------------
# Extension instances (created here so route / model files can import them)
# ---------------------------------------------------------------------------
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"  # redirect target when @login_required fails
migrate = Migrate()

# ---------------------------------------------------------------------------
# Application instance
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)


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


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html", active_page=""), 404


# ---------------------------------------------------------------------------
# Import routes & models at bottom (avoids circular imports)
# ---------------------------------------------------------------------------
from app.routes import main, auth, post, profile  # noqa: E402, F401
from app.api import posts, interactions, users     # noqa: E402, F401
from app import models                             # noqa: E402, F401

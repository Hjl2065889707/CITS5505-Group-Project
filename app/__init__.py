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
    login_manager.login_view = "auth.login"

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
        return redirect(url_for("auth.login"))

    # ── Error handlers ──

    @app.errorhandler(404)
    def page_not_found(_error):
        return render_template("404.html", active_page=""), 404

    # ── Register Blueprints ──

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.post import post_bp
    from app.routes.profile import profile_bp
    from app.api.posts import api_posts_bp
    from app.api.interactions import api_interactions_bp
    from app.api.users import api_users_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(api_posts_bp, url_prefix="/api")
    app.register_blueprint(api_interactions_bp, url_prefix="/api")
    app.register_blueprint(api_users_bp, url_prefix="/api")

    return app

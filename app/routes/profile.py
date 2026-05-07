"""Profile & Settings routes.

Owner: Hjl2065889707
"""

from flask import render_template
from app import app


@app.route("/profile")
def profile():
    """Show current user's profile page."""
    # TODO: load current_user data, support /profile/<user_id> for viewing others
    return render_template("profile.html", active_page="profile")


@app.route("/settings")
def settings():
    """Show settings page."""
    # TODO: pass SettingsForm, handle POST to save changes
    return render_template("settings.html", active_page="profile")

"""Auth routes — Login, Register, Logout.

Owner: Oliver24258175
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login page."""
    # TODO: implement login form + validation (Sprint 1)
    return render_template("login.html", active_page="")


@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration page."""
    # TODO: implement register form + validation (Sprint 1)
    return render_template("register.html", active_page="")


@app.route("/logout")
@login_required
def logout():
    """Log the current user out and redirect to feed."""
    logout_user()
    return redirect(url_for("feed"))

"""Auth routes — Login, Register, Logout.

Owner: Oliver24258175
"""

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func

from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User


def is_safe_redirect_url(target):
    """Allow redirects only to local app paths."""
    return target and target.startswith("/") and not target.startswith("//")


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for("feed"))

    form = LoginForm()

    if form.validate_on_submit():
        username_or_email = form.username_or_email.data.strip()
        identity = username_or_email.lower()
        password = form.password.data

        user = User.query.filter(
            (func.lower(User.username) == identity)
            | (func.lower(User.email) == identity)
        ).first()

        if user is None or not user.check_password(password):
            flash("Invalid username/email or password. Please try again.", "error")
            return render_template("login.html", form=form, active_page="login")

        login_user(user)
        flash(f"Welcome back, {user.username}!", "success")

        next_page = request.args.get("next")
        if is_safe_redirect_url(next_page):
            return redirect(next_page)

        return redirect(url_for("feed"))

    return render_template("login.html", form=form, active_page="login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for("feed"))

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data

        existing_username = User.query.filter(
            func.lower(User.username) == username.lower()
        ).first()
        if existing_username:
            flash("This username is already taken. Please choose another one.", "error")
            return render_template("register.html", form=form, active_page="register")

        existing_email = User.query.filter(func.lower(User.email) == email).first()
        if existing_email:
            flash("This email is already registered. Please log in instead.", "error")
            return render_template("register.html", form=form, active_page="register")

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please log in to continue.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form, active_page="register")


@app.route("/logout")
@login_required
def logout():
    """Log the current user out and redirect to feed."""
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("feed"))
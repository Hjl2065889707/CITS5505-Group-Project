"""Auth routes — Login, Register, Logout.

Owner: Oliver24258175
"""

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for("feed"))

    form = LoginForm()

    if form.validate_on_submit():
        username_or_email = form.username_or_email.data.strip()
        password = form.password.data

        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if user is None or not user.check_password(password):
            flash("Invalid username/email or password.", "error")
            return render_template("login.html", form=form, active_page="login")

        login_user(user)

        flash("You have successfully logged in.", "success")

        next_page = request.args.get("next")
        if next_page:
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

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash("This username is already taken.", "error")
            return render_template("register.html", form=form, active_page="register")

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("This email is already registered.", "error")
            return render_template("register.html", form=form, active_page="register")

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form, active_page="register")


@app.route("/logout")
@login_required
def logout():
    """Log the current user out and redirect to feed."""
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("feed"))
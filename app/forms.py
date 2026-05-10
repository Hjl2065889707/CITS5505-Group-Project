"""Flask-WTF form definitions.

Each team member adds their forms in the marked section below.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    FloatField,
    SelectField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional


# ===== Auth Forms (Oliver) ========================================


class LoginForm(FlaskForm):
    """Form for existing users to log in."""

    username_or_email = StringField(
        "Username or Email",
        validators=[
            DataRequired(message="Please enter your username or email."),
            Length(max=120),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Please enter your password."),
        ],
    )

    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    """Form for new users to create an account."""

    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Please enter a username."),
            Length(
                min=3,
                max=50,
                message="Username must be between 3 and 50 characters.",
            ),
        ],
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Please enter an email address."),
            Email(message="Please enter a valid email address."),
            Length(max=120),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Please enter a password."),
            Length(
                min=6,
                message="Password must be at least 6 characters long.",
            ),
        ],
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    submit = SubmitField("Create Account")


# ===== Post Forms (Felix) =========================================


# TODO: CreatePostForm


# ===== Settings Forms (Hjl) =======================================


# TODO: SettingsForm
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
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, NumberRange


# ===== Auth Forms (Oliver) ========================================


class LoginForm(FlaskForm):
    """Form for existing users to log in."""

    # Username or email input
    username_or_email = StringField(
        "Username or Email",
        validators=[
            DataRequired(message="Please enter your username or email."),
            Length(max=120),
        ],
    )

    # Password input
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Please enter your password."),
        ],
    )

    # Login submit button
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    """Form for new users to create an account."""

    # Username input
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

    # Email input
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Please enter an email address."),
            Email(message="Please enter a valid email address."),
            Length(max=120),
        ],
    )

    # Password input with minimum length validation
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

    # Confirm password input
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    # Register submit button
    submit = SubmitField("Create Account")


# ===== Post Forms (Felix) =========================================


class CreatePostForm(FlaskForm):
    """Form definition for creating a post."""

    content = TextAreaField(
        "Post",
        validators=[
            DataRequired(message="Please write something before posting."),
            Length(max=2000, message="Post content must be under 2000 characters."),
        ],
    )

    category = SelectField(
        "Category",
        choices=[
            ("Catch Report", "Catch Report"),
            ("Gear Review", "Gear Review"),
            ("Question", "Question"),
            ("General", "General"),
        ],
        validators=[
            DataRequired(message="Please select a category."),
        ],
    )

    species = StringField(
        "Species",
        validators=[
            Optional(),
            Length(max=120, message="Species must be under 120 characters."),
        ],
    )

    weight_kg = FloatField(
        "Weight (kg)",
        validators=[
            Optional(),
            NumberRange(min=0, message="Weight cannot be negative."),
        ],
    )

    bait = StringField(
        "Bait",
        validators=[
            Optional(),
            Length(max=120, message="Bait must be under 120 characters."),
        ],
    )

    location_name = StringField(
        "Location",
        validators=[
            Optional(),
            Length(max=120, message="Location must be under 120 characters."),
        ],
    )

    latitude = FloatField(
        "Latitude",
        validators=[
            Optional(),
            NumberRange(min=-90, max=90, message="Latitude must be between -90 and 90."),
        ],
    )

    longitude = FloatField(
        "Longitude",
        validators=[
            Optional(),
            NumberRange(min=-180, max=180, message="Longitude must be between -180 and 180."),
        ],
    )

    submit = SubmitField("Post")
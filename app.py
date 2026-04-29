import json
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, render_template


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
POSTS_FILE = BASE_DIR / "mockdata" / "myPosts.json"


def format_date(date_value):
    if not date_value:
        return "Unknown date"

    try:
        parsed_date = datetime.fromisoformat(date_value.replace("Z", "+00:00"))
        return parsed_date.strftime("%d %b %Y")
    except ValueError:
        return date_value


def load_posts():
    with POSTS_FILE.open("r", encoding="utf-8") as file:
        posts = json.load(file)

    for post in posts:
        post["displayDate"] = format_date(post.get("createdAt"))

    return posts


def get_post_by_id(post_id):
    posts = load_posts()

    for post in posts:
        if post.get("id") == post_id:
            return post

    return None


@app.route("/")
def feed():
    posts = load_posts()
    return render_template("feed.html", posts=posts, active_page="feed")


@app.route("/posts/<post_id>")
def post_detail(post_id):
    post = get_post_by_id(post_id)

    if post is None:
        abort(404)

    comments = [
        {
            "username": "RiverKing",
            "avatarUrl": "https://images.pexels.com/photos/775358/pexels-photo-775358.jpeg",
            "time": "2 hours ago",
            "text": "Nice catch! That looks like a great spot.",
        }
    ]

    return render_template(
        "post_detail.html",
        post=post,
        comments=comments,
        active_page="post",
    )


@app.route("/404-demo")
def demo_404():
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", active_page=""), 404


if __name__ == "__main__":
    app.run(debug=True)
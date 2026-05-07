"""Post detail route.

Owner: Hjl2065889707
"""

import json
from pathlib import Path

from flask import render_template, abort
from app import app


# ---------- Temporary mock-data helpers (remove after DB migration) ----------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
POSTS_FILE = BASE_DIR / "mockdata" / "myPosts.json"


def _load_posts():
    with POSTS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def _get_post_by_id(post_id):
    for p in _load_posts():
        if p.get("id") == post_id:
            return p
    return None


# ---------- Routes ----------


@app.route("/posts/<post_id>")
def post_detail(post_id):
    """Show a single post with its details."""
    # TODO: replace mock lookup with Post.query.get_or_404(post_id)
    post = _get_post_by_id(post_id)
    if post is None:
        abort(404)
    return render_template("post_detail.html", post=post, active_page="feed")

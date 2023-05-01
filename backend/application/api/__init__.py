from flask import Blueprint, jsonify
from datetime import datetime, timedelta

bp = Blueprint("api", __name__)


@bp.route("/")
def index():
    return jsonify({
        "status": 200,
        "message": "Welcome to Astra Chatbot"
    })


def now(day=0):
    return (datetime.now() + timedelta(days=1) * day).replace(
        microsecond=0).isoformat()


reserved_words = [
    "admin", "omni", "user", "users", "store", "stores", "item",
    "items"]  # property, cart, save


training_template = {
    "key": None,
    "created_at": None,
    "updated_at": None,
    "type": "training",
    "question": None,
    "answer": None
}


def training_schema(p):
    photos = []
    if "photos" in p:
        for photo in p['photos']:
            photos.append(f"/photo/{photo}")

    return {
        "status": p["status"],
        "title": p["title"],
        "format": p["format"],
        "photos": photos,
        "videos": p["videos"] if "videos" in p else [],
        "description": p["description"],
        "content": p["content"],
        "slug": p["slug"],
        "tags": p["tags"],
        "comments": p['comments'] if "comments" in p else [],
        "type": p["type"],
        "created_at": p["created_at"],
    }

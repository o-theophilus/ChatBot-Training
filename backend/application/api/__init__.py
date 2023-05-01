from flask import Blueprint, jsonify
from datetime import datetime, timedelta


bp = Blueprint("api", __name__)


@bp.route("/")
def index():
    return jsonify({
        "status": 200,
        "message": "Welcome to Chatbot"
    })


def now(day=0):
    return (datetime.now() + timedelta(days=1) * day).replace(
        microsecond=0).isoformat()

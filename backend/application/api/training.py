from flask import Blueprint, jsonify, request
from . import db, now
# from .interview import interview
from uuid import uuid4

bp = Blueprint("training", __name__)


@bp.post("/training")
def post():

    message = {}
    if "question" not in request.json or not request.json["question"]:
        message["question"] = "cannot be empty"
    if "answer" not in request.json or not request.json["answer"]:
        message["answer"] = "cannot be empty"

    if message != {}:
        return jsonify({
            "status": 201,
            "message": message
        })

    db.add({
        "key": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),
        "type": "training",
        "question": request.json["question"],
        "answer": request.json["answer"]
    })

    return jsonify({
        "status": 200,
        "message": "successful",
    })

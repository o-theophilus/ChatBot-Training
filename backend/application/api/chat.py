from flask import Blueprint, jsonify, request
from llama_index import GPTSimpleVectorIndex
from . import db, now
from uuid import uuid4

bp = Blueprint("chat", __name__)


@bp.post("/chat")
def post():

    if "say" not in request.json or not request.json["say"]:
        return jsonify({
            "status": 201,
            "message": "cannot be empty"
        })

    brain = db.get_brain()["data"]
    brain = GPTSimpleVectorIndex.load_from_string(brain)

    response = brain.query(
        request.json["say"],
        response_mode="compact"
    )

    learn(request.json["say"], response.response)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "response": response.response
        }
    })


def learn(user, bot):
    db.add({
        "key": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),
        "type": "learning",
        "user": user,
        "bot": bot
    })

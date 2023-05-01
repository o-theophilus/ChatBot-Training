from flask import Blueprint, jsonify, request
from llama_index import GPTSimpleVectorIndex
from . import db, now
from uuid import uuid4

bp = Blueprint("chat", __name__)


@bp.post("/chat")
def post():

    if "message" not in request.json or not request.json["message"]:
        return jsonify({
            "status": 201,
            "message": "cannot be empty"
        })

    brain = db.get_brain()["data"]
    brain = GPTSimpleVectorIndex.load_from_string(brain)

    response = brain.query(
        request.json["message"],
        response_mode="compact"
    )

    data = db.data()

    learning = None
    for row in data:
        if row["type"] == "learning":
            row["data"] = f"""{row["data"]}
user: {request.json["message"]}
chatbot: {response.response}
"""
            learning = row
            break

    if not learning:
        learning = {
            "key": uuid4().hex,
            "created_at": now(),
            "updated_at": now(),
            "type": "learning",
            "data": f"""
user: {request.json["message"]}
chatbot: {response.response}
"""
        }

        data.append(learning)

    db.add(learning)

    return jsonify({
        "status": 200,
        "message": "successful",
        "response": response.response
    })

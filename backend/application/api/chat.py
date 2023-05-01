from flask import Blueprint, jsonify, request
from llama_index import GPTSimpleVectorIndex
from . import db  # , dd
# import io

bp = Blueprint("chat", __name__)


@bp.post("/chat")
def post():

    if "say" not in request.json or not request.json["say"]:
        return jsonify({
            "status": 201,
            "message": "cannot be empty"
        })

    # index = dd.get("index.json")
    # index = io.BytesIO(index.read()).getvalue().decode('utf-8')
    index = db.get_type("index")[0]["data"]
    index = GPTSimpleVectorIndex.load_from_string(index)

    response = index.query(
        request.json["say"],
        response_mode="compact"
    )

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "response": response.response
        }
    })

from flask import Blueprint, jsonify, request
from . import db, now
from uuid import uuid4


bp = Blueprint("training", __name__)


def training_template(question, answer):
    return {
        "key": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),
        "type": "training",
        "question": question,
        "answer": answer
    }


# def training_schema(p):
#     photos = []
#     if "photos" in p:
#         for photo in p['photos']:
#             photos.append(f"/photo/{photo}")

#     return {
#         "status": p["status"],
#         "title": p["title"],
#         "format": p["format"],
#         "photos": photos,
#         "videos": p["videos"] if "videos" in p else [],
#         "description": p["description"],
#         "content": p["content"],
#         "slug": p["slug"],
#         "tags": p["tags"],
#         "comments": p['comments'] if "comments" in p else [],
#         "type": p["type"],
#         "created_at": p["created_at"],
#     }


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

    db.add(training_template(
        request.json["question"],
        request.json["answer"]
    ))

    return jsonify({
        "status": 200,
        "message": "successful",
    })

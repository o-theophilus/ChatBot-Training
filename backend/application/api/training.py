from flask import Blueprint, jsonify, request
from . import db, now
from uuid import uuid4
from brain import build_brain


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


def training_schema(t):
    return {
        "key": t["key"],
        "created_at": t["created_at"],
        "updated_at": t["updated_at"],
        "type": t["type"],
        "question": t["question"],
        "answer": t["answer"]
    }


@bp.get("/training/<key>")
def get(key):
    training = db.key(key)
    if not training:
        return jsonify({
            "status": 401,
            "message": "invalid request",
        })

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "training": training_schema(training)
        }
    })


@bp.get("/training")
def get_all():
    trainings = db.get_type("training")

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "trainings": [training_schema(t) for t in trainings]
        }
    })


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

    build_brain()

    return jsonify({
        "status": 200,
        "message": "successful",
    })


@bp.put("/training/<key>")
def put(key):

    error = {}
    if "question" not in request.json or not request.json["question"]:
        error["question"] = "cannot be empty"
    if "answer" not in request.json or not request.json["answer"]:
        error["answer"] = "cannot be empty"
    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    data = db.data()

    training = None
    for row in data:
        if row["key"] == key:
            row["question"] = request.json["question"]
            row["answer"] = request.json["answer"]
            training = row
            break

    if not training:
        return jsonify({
            "status": 401,
            "message": "invalid request",
        })

    db.add(training)
    build_brain(data)

    return jsonify({
        "status": 200,
        "message": "successful",
    })


@bp.delete("/training/<key>")
def delete(key):

    data = db.data()

    training = None
    for row in data:
        if row["key"] == key:
            training = row
            db.rem(row["key"])
            data.remove(row)
            break

    if not training:
        return jsonify({
            "status": 401,
            "message": "invalid request",
        })

    build_brain(data)

    return jsonify({
        "status": 200,
        "message": "successful",
    })

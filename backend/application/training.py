from flask import Blueprint, jsonify, request
from . import db
from uuid import uuid4
from .brain import build_brain


bp = Blueprint("training", __name__)


def training_template(training):
    return {
        "key": uuid4().hex,
        "created_at": db.now(),
        "updated_at": db.now(),
        "type": "training",
        "data": training,
    }


def training_schema(t):
    return {
        "key": t["key"],
        "created_at": t["created_at"],
        "updated_at": t["updated_at"],
        "data": t["data"]
    }


@bp.get("/training")
def get():
    data = db.data()

    training = None
    for row in data:
        if row["type"] == "training":
            training = row
            break

    return jsonify({
        "status": 200,
        "message": "successful",
        "training": training_schema(training)
    })


@bp.post("/training")
def post():

    error = {}
    if "openai_api_key" not in request.json or not request.json[
            "openai_api_key"]:
        error["openai_api_key"] = "cannot be empty"
    if "training" not in request.json or not request.json["training"]:
        error["training"] = "cannot be empty"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    data = db.data()

    training = None
    for row in data:
        if row["type"] == "training":
            row["data"] = request.json["training"]
            row["updated_at"] = db.now()
            training = row
            break

    try:
        build_brain(training["data"], data)
    except Exception as e:
        return jsonify({
            "status": 201,
            "message": {
                "openai_api_key": str(e.last_attempt.exception())
            }
        })

    db.add(training)

    return jsonify({
        "status": 200,
        "message": "successful",
        "training": training
    })


@bp.delete("/training")
def reset():
    if "openai_api_key" not in request.json or not request.json[
            "openai_api_key"]:
        return jsonify({
            "status": 201,
            "message": {
                "openai_api_key": "cannot be empty"
            }
        })

    data = db.data()

    training = None
    reset = None
    for row in data:
        if row["type"] == "training":
            training = row
        elif row["type"] == "reset":
            reset = row
        if training and reset:
            break

    try:
        build_brain(reset["data"], data)
    except Exception as e:
        return jsonify({
            "status": 201,
            "message": {
                "openai_api_key": str(e.last_attempt.exception())
            }
        })

    training["data"] = reset["data"]
    db.add(training)

    return jsonify({
        "status": 200,
        "message": "successful",
        "training": training
    })

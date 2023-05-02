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

    if not training:
        training = db.add(training_template(""))
        data.append(training)
        build_brain(data)

    return jsonify({
        "status": 200,
        "message": "successful",
        "training": training_schema(training)
    })


@bp.post("/training")
def post():

    if "training" not in request.json or not request.json["training"]:
        return jsonify({
            "status": 201,
            "message": "cannot be empty"
        })

    data = db.data()

    training = None
    for row in data:
        if row["type"] == "training":
            row["data"] = request.json["training"]
            row["updated_at"] = db.now()
            training = row
            break

    db.add(training)
    build_brain(data)

    return jsonify({
        "status": 200,
        "message": "successful",
        "training": training
    })


@bp.delete("/training")
def reset():

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

    if not training or not reset:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    training["data"] = reset["data"]
    db.add(training)
    build_brain(data)

    return jsonify({
        "status": 200,
        "message": "successful",
        "training": training
    })

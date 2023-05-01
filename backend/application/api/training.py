from flask import Blueprint, jsonify, request
from . import db, now
from uuid import uuid4
from .brain import build_brain


bp = Blueprint("training", __name__)


def training_template(training):
    return {
        "key": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),
        "type": "training",
        "data": training,
    }


def training_schema(t):
    return {
        "key": t["key"],
        "created_at": t["created_at"],
        "updated_at": t["updated_at"],
        # "type": t["type"],
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
            training = row
            break

    db.add(training)
    build_brain(data)

    return jsonify({
        "status": 200,
        "message": "successful",
        "training": training
    })


@bp.get("/fix")
def fix():
    data = db.data()

    training = ""
    for row in data:
        if row["type"] == "training":
            training = f"""{training}
question: {row["question"]}
answer: {row["answer"]}
            """

    print("#"*80)
    print("#"*80)
    print(training)
    # if not training:
    #     training = training_template(
    #         request.json["training"]
    #     )
    #     data.append(training)

    # db.add(training)

    return jsonify({
        "status": 200,
        "message": "successful",
    })

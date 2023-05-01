from flask import current_app
from deta import Deta


def drive():
    name = "chatbot"
    # if current_app.config["DEBUG"]:
    #     name = "test"
    return Deta(current_app.config["DETA_KEY"]).Drive(name)


def add(file, path=""):
    drive().put(f"/{path}/index.json", file)


def rem(name, path=""):
    return drive().delete(f"/{path}/{name}")


def get(name, path=""):
    return drive().get(f"/{path}/{name}")

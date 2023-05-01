from flask import current_app
from deta import Deta


def base():
    return Deta(current_app.config["DETA_KEY"]).Base("live")


def data():
    res = base().fetch()
    items = res.items

    while res.last:
        res = base().fetch(last=res.last)
        items += res.items

    return items


def get_brain(db=None):
    if not db:
        db = data()
    for row in db:
        if "type" in row and row["type"] == "brain":
            return row
    return None


def add(x):
    return base().put(x)


def add_many(x):
    return base().put_many(x)

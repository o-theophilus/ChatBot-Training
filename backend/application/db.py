from flask import current_app
from deta import Deta
from datetime import datetime, timedelta


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


def now(day=0):
    return (datetime.now() + timedelta(days=1) * day).replace(
        microsecond=0).isoformat()

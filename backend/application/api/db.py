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


def key(key, db=None):
    if not db:
        db = data()

    for row in db:
        if row["key"] == key:
            return row
    return None


# def get(type_, ppt, val, db=None):
#     if not db:
#         db = data()
#     item = None
#     for row in db:
#         if "type" in row and ppt in row:
#             if row["type"] == type_ and row[ppt] == val:
#                 item = row
#                 break
#     return item


def get_type(type_, db=None):
    if not db:
        db = data()
    items = []
    for row in db:
        if "type" in row and row["type"] == type_:
            items.append(row)
    return items


def add(x):
    return base().put(x)


# def add_many(x):
#     return base().put_many(x)


def rem(key):
    return base().delete(key)

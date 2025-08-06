from flask import session

def create_session(username, roles, code=None, identifier=None):
    session["user"] = username
    session["roles"] = roles
    session["code"] = code
    session["identifier"] = identifier


def erase_session():
    del session["user"]
    del session["roles"]
    if session.get("code"):
        del session["code"]
    else:
        del session["identifier"]

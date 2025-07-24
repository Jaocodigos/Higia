from flask import session

def create_session(username, role, code, identifier):
    session["user"] = username
    session["role"] = role
    session["code"] = code
    session["identifier"] = identifier

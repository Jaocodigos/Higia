from flask import json
from werkzeug.exceptions import HTTPException
from engine.app.factory import app


class HandlerManager(object):

    # Function to be called when the error not call any created handler.
    def not_handler(self):
        ...

    def handle(self):
        ...


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


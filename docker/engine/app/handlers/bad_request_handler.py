from werkzeug.exceptions import BadRequest
from engine.app.handlers.handlers import HandlerManager
from flask import request, flash, jsonify, url_for, redirect
from engine.app.config.logs import prepare_logs


class BadRequestHandler(HandlerManager):

    def __init__(self):
        super().__init__(prepare_logs(__name__))

    @property
    def code(self):
        return BadRequest.code

    def json(self, e):
        response = {
            "message": "The server could not understand the request sent. Some inserted data is invalid.",
            "detail": e.description
        }
        return jsonify(response)

from werkzeug.exceptions import Conflict
from engine.app.handlers.handlers import HandlerManager
from flask import request, flash, jsonify, url_for, redirect
from engine.app.config.logs import prepare_logs


class ConflictHandler(HandlerManager):

    def __init__(self):
        super().__init__(prepare_logs(__name__))

    @property
    def code(self):
        return Conflict.code

    def json(self, e):
        response = {
            "message": "Something unexpected happen on our services. Try again later."
        }
        return jsonify(response)

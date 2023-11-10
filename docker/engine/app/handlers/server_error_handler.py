from werkzeug.exceptions import InternalServerError
from engine.app.handlers.handlers import HandlerManager
from flask import request, flash, jsonify, url_for, redirect
from engine.app.config.logs import prepare_logs


class ServerHandler(HandlerManager):

    def __init__(self):
        super().__init__(prepare_logs(__name__))

    @property
    def code(self):
        return InternalServerError.code

    def html(self, e):
        return redirect(url_for('view.login'))

    def json(self, e):
        response = {
            "message": f"Something unexpected happen when performing request {request.path}",
            "detail": e.description
        }
        return jsonify(response)

from werkzeug.exceptions import NotFound
from engine.app.handlers.handlers import HandlerManager
from flask import request, flash, jsonify, url_for, redirect
from engine.app.config.logs import prepare_logs


class NotFoundHandler(HandlerManager):

    def __init__(self):
        super().__init__(prepare_logs(__name__))

    @property
    def code(self):
        return NotFound.code

    def html(self, e):
        return redirect(url_for('view.login'))

    def json(self, e):
        response = {
            "message": "The requested page not exist."
        }
        return jsonify(response)

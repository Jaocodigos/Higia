from werkzeug.exceptions import Unauthorized
from engine.app.handlers.handlers import HandlerManager
from flask import request, flash, jsonify, url_for, redirect
from engine.app.config.logs import prepare_logs


class UnauthorizedHandler(HandlerManager):

    def __init__(self):
        super().__init__(prepare_logs(__name__))

    @property
    def code(self):
        return Unauthorized.code

    # Create a error template in future
    def html(self, e):
        flash("Access denied.", "error")
        return redirect(url_for("view.login"))

    def json(self, e):
        response = {
            "message": f"Access denied, please verify your credentials to access {request.path}"
        }
        return jsonify(response)

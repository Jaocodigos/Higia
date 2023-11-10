from flask import json, jsonify, request, render_template, redirect, url_for
from werkzeug.exceptions import default_exceptions
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


def handle_default_exceptions(e):
    if hasattr(request, 'headers') and 'html' in request.headers.get('Accept', []):
        if e.code == 401:
            return render_template('errors/401.html'), 401
        elif e.code == 404:
            return render_template('errors/404.html'), 404
        else:
            return redirect(url_for('view.login'))
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "message": e.description,
    })
    response.content_type = "application/json"
    return response


def handle_unexpected_exception(e):
    if hasattr(request, 'headers') and 'html' in request.headers.get('Accept', []):
        template_500 = 'errors/500.html'
        if hasattr(request, 'app') and request.app:
            template_500 = request.app.error_500_html or template_500
        return render_template(template_500), 500
    return jsonify({
        "code": 500,
        "name": "Internal Server Error",
        "message": "The server encountered an internal error and was unable to complete your request."
                   " Either the server is overloaded or there is an error in the application.",
    }), 500


def register_exception_handlers(app):
    for ex in default_exceptions:
        app.register_error_handler(ex, handle_default_exceptions)
    app.register_error_handler(Exception, handle_unexpected_exception)

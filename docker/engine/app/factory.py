from engine.app.models import db
from engine.app.config.environment import get_flask_config
from flask import Flask
import logging

log = logging.getLogger("Higia." + __name__)

app = Flask(__name__)


def init_app():
    log.debug("Getting environment for config.")
    app.config.from_object(get_flask_config())

    log.debug("Init database.")
    db.init_app(app)

    log.debug("Registering blueprints.")
    from engine.app.resources.api import api
    from engine.app.resources.frontend import view
    app.register_blueprint(api)
    app.register_blueprint(view)

    log.info("Application is running!")
    return app

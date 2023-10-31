from engine.app.models import db
from engine.app.config.environment import get_flask_config
from engine.app.config.swagger_specs import APIDocs, set_swagger_config
from flask import Flask
from flask_migrate import Migrate
from engine.app.schemas import ma
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)

app = Flask(__name__)


def init_app():
    log.debug("Getting environment for config.")
    app.config.from_object(get_flask_config())

    log.debug("Init database.")
    db.init_app(app)
    Migrate(app, db, directory="migrations")

    log.debug("Init Marshmallow")
    ma.init_app(app)

    log.debug("Registering blueprints.")
    from engine.app.resources.api import api
    from engine.app.resources.frontend import view
    app.register_blueprint(api)
    app.register_blueprint(view)

    log.debug("Adding Swagger.")
    set_swagger_config(app)
    APIDocs(app, template_file="swagger.yaml")

    log.info("Application is running!")
    return app

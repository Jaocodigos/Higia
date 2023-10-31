from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.settings import Settings
from flask import request, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.schemas.settings.settings_schema import SettingsSchema
from engine.app.models import db
from engine.app.config.default import set_default_db_config
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


@api.get('/settings')
@api_auth(roles=['administrator', 'patient'])
def get_config():
    log.info('Retrieving system configs.')
    settings = Settings.query.first_or_404()
    log.debug(f'Returning config: {settings}')
    return jsonify({'Actual System Configuration': settings.serialized()}), 200


@api.post('/settings')
@api_auth(roles=['administrator'])
def new_config():
    log.info('Providing a new configuration to system.')
    data = request.json
    settings = Settings.query.first_or_404()
    new_settings = convert_json_to_model(settings, SettingsSchema(), data)
    log.debug(f'Settings updated!')
    return new_settings, 201


@api.get('/testing')
@api_auth(roles=['administrator'])
def testing_mode():
    log.info('Creating all models to start testing.')
    try:
        db.create_all()
        set_default_db_config()
    except Exception as e:
        exit(f"Models can't be registered. {e}")
    log.debug(f'Models registered!')
    return {'Status': 'Created!'}

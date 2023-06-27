from engine.app.resources.api import api
from engine.app.services.authentication import api_auth
from engine.app.models.intern.settings import Settings
from flask import request, abort, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.schemas.settings.settings_schema import SettingsSchema
import logging

log = logging.getLogger("Higia." + __name__)


@api.route('/settings', methods=['GET'])
@api_auth(roles=['administrator', 'users'])
def get_config():
    log.info('Retrieving system configs.')
    settings = Settings.query.first()
    log.debug(f'Returning config: {settings}')
    return jsonify({'Actual System Configuration': settings.serialized}), 200


@api.route('/settings', methods=['POST'])
@api_auth(roles=['administrator'])
def new_config():
    log.info('Providing a new configuration to system.')
    data = request.json
    settings = Settings.query.first_or_404()
    user = convert_json_to_model(settings, SettingsSchema(), data)
    log.debug(f'Settings updated!')
    return user, 201


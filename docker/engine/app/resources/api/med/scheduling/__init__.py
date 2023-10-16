from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.scheduling import Scheduling
from flask import request, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.schemas.users.user_schema import UserUpdateSchema
import logging

log = logging.getLogger("Higia." + __name__)


@api.get('/schedules')
@api_auth(roles=['administrator'])
def list_schedules():
    log.info('Retrieving doctor schedulers.')
    schedulers = Scheduling.query.all()
    log.debug(f'Returning schedulers: {schedulers}')
    return jsonify({'Users': [x.serialized(x.protected_fields) for x in schedulers]}), 200


@api.put('/schedules/<string:identifier>')
@api_auth(roles=['administrator'])
def edit_scheduling(identifier):
    log.info(f'Altering scheduling data for user with identifier: {identifier}.')
    user = Scheduling.query.filter_by(identifier=identifier).first_or_404()
    data = request.json
    updated_user = convert_json_to_model(user, UserUpdateSchema(), data)
    log.debug(f'User data altered!')
    return updated_user, 200


@api.delete('/schedules/<string:identifier>')
@api_auth(roles=['administrator'])
def exclude_scheduling(identifier):
    log.info(f'Deleting scheduling {identifier}.')
    user = Scheduling.query.filter_by(identifier=identifier).first_or_404()
    log.debug(f'Deleting user with ID: {user.id}')
    user.delete()
    log.info("User deleted!")
    return jsonify({'Status': 'Deleted!'}), 200

from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.users import Users
from flask import request, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.schemas.schedulers.schedule_schema import ScheduleUpdateSchema
import logging

log = logging.getLogger("Higia." + __name__)


@api.get('/schedules')
@api_auth(roles=['doctor'])
def list_schedules(doctor):
    log.info(f'Retrieving doctor {doctor.username} schedulers.')
    doctor = Users.query.filter_by(identifier=doctor.identifier).first_or_404()
    schedulers = doctor.doctor_schedulers
    log.debug(f'Schedulers: {len(schedulers)}')
    return jsonify({'Schedules': [x.serialized(x.protected_fields) for x in schedulers]}), 200


@api.put('/schedules/<string:identifier>')
@api_auth(roles=['doctor'])
def edit_scheduling(doctor, identifier):
    log.info(f'Altering scheduling data of user with identifier: {identifier}. Requested by doctor {doctor.username}')
    doctor = Users.query.filter_by(identifier=doctor.identifier).first_or_404()
    data = request.json
    updated_schedule = convert_json_to_model(doctor, ScheduleUpdateSchema(), data)
    log.debug(f'Schedule data altered!')
    return updated_schedule, 200


@api.delete('/schedules/<string:identifier>')
@api_auth(roles=['doctor'])
def exclude_scheduling(doctor, identifier):
    log.info(f'Deleting schedule of user {identifier}. Requested by doctor {doctor.username}')
    doctor = Users.query.filter_by(identifier=doctor.identifier).first_or_404()
    log.debug(f'Deleting doctor schedule with identifier: {identifier}')
    try:
        schedule = list(filter(lambda x: x.patient_identifier == identifier, doctor.doctor_schedulers))[0]
        schedule.delete()
    except Exception as e:
        log.error(f"Error while finding and deleting schedule of user {identifier}: {e}")
        return jsonify({'Status': 'Conflict!'}), 409
    log.info("User deleted!")
    return jsonify({'Status': 'Deleted!'}), 200

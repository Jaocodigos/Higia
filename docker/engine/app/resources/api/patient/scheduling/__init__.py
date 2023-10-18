from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.users import Users
from flask import request, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.schemas.schedulers.schedule_schema import ScheduleSchema
import logging

log = logging.getLogger("Higia." + __name__)


@api.get('/patient/schedules')
@api_auth(roles=['patient'])
def show_schedules(patient):
    log.info(f'Retrieving doctor {patient.username} schedulers.')
    patient = Users.query.filter_by(identifier=patient.identifier).first_or_404()
    schedulers = patient.patient_schedulers
    log.debug(f'Schedulers: {len(schedulers)}')
    return jsonify({'Schedules': [x.serialized(x.protected_fields) for x in schedulers]}), 200


@api.post('/patient/schedules')
@api_auth(roles=['patient'])
def mark_schedule(patient):
    log.info(f'Creating a schedule for user with identifier: {patient.identifier}.')
    doctor = Users.query.filter_by(identifier=patient.identifier).first_or_404()
    data = request.json
    schedule = convert_json_to_model(doctor, ScheduleSchema(), data)
    log.debug(f'Schedule data altered!')
    return schedule, 201


@api.delete('/patient/schedules/<string:schedule_id>')
@api_auth(roles=['patient'])
def markoff_schedule(patient, schedule_id):
    log.info(f'Deleting schedule of user {patient.identifier}.')
    patient = Users.query.filter_by(identifier=patient.identifier).first_or_404()
    log.debug(f'Deleting patient schedule with identifier: {patient.identifier}')
    try:
        schedule = list(filter(lambda x: x.id == schedule_id, patient.patient_schedulers))[0]
        schedule.delete()
    except Exception as e:
        log.error(f"Error while finding and deleting schedule of user {patient.identifier}: {e}")
        return jsonify({'Status': 'Conflict!'}), 409
    log.info("User deleted!")
    return jsonify({'Status': 'Deleted!'}), 200

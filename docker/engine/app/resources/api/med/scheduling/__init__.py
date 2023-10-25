from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.collaborators import Collaborators
from engine.app.models.intern.scheduling import Scheduling
from flask import request, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.schemas.schedulers.schedule_schema import ScheduleUpdateSchema
import logging

log = logging.getLogger("Higia." + __name__)


@api.get('/schedules')
@api_auth(roles=['doctor'])
def list_schedules(doctor):
    log.info(f'Retrieving doctor {doctor.username} schedulers.')
    doctor = Collaborators.query.filter_by(identifier=doctor.identifier).first_or_404()
    schedulers = doctor.doctor_schedulers
    log.debug(f'Schedulers: {len(schedulers)}')
    return jsonify({'Schedules': [x.serialized(x.protected_fields) for x in schedulers]}), 200


@api.put('/schedules/<string:schedule_id>')
@api_auth(roles=['doctor'])
def edit_scheduling(doctor, schedule_id):
    log.info(f'Altering scheduling data. Requested by doctor {doctor.username}')
    schedule = Scheduling.query.filter_by(id=schedule_id).first_or_404()
    data = request.json
    updated_schedule = convert_json_to_model(schedule, ScheduleUpdateSchema(), data)
    log.debug(f'Schedule data altered!')
    return updated_schedule, 200


@api.delete('/schedules/<string:schedule_id>')
@api_auth(roles=['doctor', 'patient'])
def exclude_scheduling(user, schedule_id):
    log.info(f'Deleting schedule. Requested by user {user.username} with identifier {user.identifier}')
    schedule = Scheduling.query.filter_by(id=schedule_id).first_or_404()
    log.debug(f'Deleting doctor schedule with id: {schedule_id}')
    schedule.delete()
    log.info("User deleted!")
    return jsonify({'Status': 'Deleted!'}), 200

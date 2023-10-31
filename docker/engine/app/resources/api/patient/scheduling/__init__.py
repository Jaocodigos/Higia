from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.patients import Patients
from engine.app.models.intern.collaborators import Collaborators
from engine.app.models.intern.scheduling import Scheduling
from flask import request, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.utils.converters.convert_dates import convert_string_date_to_datetime
from engine.app.schemas.schedulers.schedule_schema import ScheduleSchema
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


@api.get('/patient/schedules')
@api_auth(roles=['patient'])
def show_schedules(patient):
    log.info(f'Retrieving patient {patient.username} schedulers.')
    patient = Patients.query.filter_by(identifier=patient.identifier).first_or_404()
    schedulers = patient.patient_schedulers
    log.debug(f'Schedulers: {len(schedulers)}')
    return jsonify({'Schedules': [x.serialized(x.protected_fields) for x in schedulers]}), 200


@api.post('/patient/schedules/<string:doctor_id>')
@api_auth(roles=['patient'])
def mark_schedule(patient, doctor_id):
    log.info(f'Creating a schedule for user with identifier: {patient.identifier}.')
    doctor = Collaborators.query.filter_by(id=doctor_id).with_entities(Collaborators.full_name).first_or_404()
    patient_data = Patients.query.filter_by(identifier=patient.identifier).with_entities(Patients.id).first_or_404()
    data = request.json
    data['doctor_name'] = doctor.full_name
    data['doctor'] = doctor_id
    data['patient'] = patient_data.id
    data['patient_name'] = patient.username
    data['patient_identifier'] = patient.identifier
    schedule = convert_json_to_model(Scheduling(), ScheduleSchema(), data,
                                     converters={'appointment_day': convert_string_date_to_datetime})
    log.debug(f'Schedule data altered!')
    return schedule, 201

from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.patients import Patients
from flask import jsonify
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


@api.get('/patient/exams')
@api_auth(roles=['patient'])
def show_exams(patient):
    log.info(f'Retrieving patient {patient.username} scheduled exams.')
    patient = Patients.query.filter_by(identifier=patient.identifier).first_or_404()
    exams = patient.patient_exams
    log.debug(f'Schedulers: {len(exams)}')
    return jsonify({'Exams': [x.serialized(x.protected_fields) for x in exams]}), 200

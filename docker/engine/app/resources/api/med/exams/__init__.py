from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.exams import Exams
from engine.app.models.intern.users import Users
from flask import request, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.utils.converters.convert_user_datas import convert_identifier
from engine.app.utils.converters.convert_dates import convert_string_date_to_datetime
from engine.app.schemas.exams.exam_schema import ExamSchema, ExamUpdateSchema
import logging

log = logging.getLogger("Higia" + __name__)


@api.get('/exams')
@api_auth(roles=['doctor'])
def list_exams(doctor):
    log.info(f'Retrieving exams registered by Dr. {doctor.username}.')
    doctor = Users.query.filter_by(identifier=doctor.identifier).first_or_404()
    log.debug(f'Total exams: {len(doctor.doctor_exams)}')
    return jsonify({'Exams': [x.serialized(x.protected_fields) for x in doctor.doctor_exams]}), 200


@api.post('/exams')
@api_auth(roles=['doctor'])
def add_exam(doctor):
    log.info(f'Creating a new user. Requested by Dr. {doctor.username}.')
    data = request.json
    patient = Users.query.filter_by(identifier=data.get('patient_identifier')).first_or_404()
    doctor = Users.query.filter_by(identifier=doctor.identifier).first_or_404(description="Patient not found.")
    data['patient'] = patient.id
    data['patient_name'] = patient.full_name
    data['doctor'] = doctor.id
    data['doctor_name'] = doctor.full_name
    exam = convert_json_to_model(Exams(), ExamSchema(), data, converters={'patient_identifier': convert_identifier,
                                                                          'exam_date': convert_string_date_to_datetime,
                                                                          'validity': convert_string_date_to_datetime})
    log.debug(f'Exam created: {exam}')
    return exam, 201


@api.put('/exams/<string:exam_id>')
@api_auth(roles=['doctor'])
def edit_exam(doctor, exam_id):
    log.info(f'Altering exam: {exam_id}. Requested by Dr. {doctor.username}.')
    exam = Exams.query.filter_by(id=exam_id).first_or_404()
    data = request.json
    updated_exam = convert_json_to_model(exam, ExamUpdateSchema(), data,
                                         converters={'patient_identifier': convert_identifier,
                                                     'exam_date': convert_string_date_to_datetime,
                                                     'validity': convert_string_date_to_datetime
                                                     })
    log.debug(f'Exam data altered!')
    return updated_exam, 200


@api.delete('/exams/<string:exam_id>')
@api_auth(roles=['doctor'])
def exclude_exam(doctor, exam_id):
    log.info(f'Deleting exam {exam_id}. Requested by Dr. {doctor.username}.')
    exam = Exams.query.filter_by(id=exam_id).first_or_404()
    exam.delete()
    log.info("Exam deleted!")
    return jsonify({'Status': 'Deleted!'}), 200

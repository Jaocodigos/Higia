from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.exams import Exams
from engine.app.models.intern.users import Users
from flask import request, jsonify, session
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.utils.converters.convert_user_datas import convert_identifier
from engine.app.schemas.exams.exam_schema import ExamSchema, ExamUpdateSchema
import logging

log = logging.getLogger("Higia." + __name__)


@api.get('/exams')
@api_auth(roles=['doctor'])
def list_exams():
    log.info('Retrieving exams registered by doctor.')
    doctor_id = session.get('user_id')
    doctor = Users.query.filter_by(id=doctor_id).first_or_404()
    log.debug(f'Returning exams: {doctor.exams}')
    return jsonify({'Exams': [x.serialized for x in doctor.exams]}), 200


@api.post('/exams')
@api_auth(roles=['doctor'])
def add_exam():
    log.info('Creating a new user.')
    data = request.json
    exam = convert_json_to_model(Exams(), ExamSchema(), data, converters={'patient_identifier': convert_identifier})
    log.debug(f'Exam created: {exam}')
    return exam, 201


@api.put('/exams/<string:id>')
@api_auth(roles=['doctor'])
def edit_exam(exam_id):
    log.info(f'Altering exam: {exam_id}.')
    exam = Exams.query.filter_by(id=exam_id).first_or_404()
    data = request.json
    updated_exam = convert_json_to_model(exam, ExamUpdateSchema(), data, converters={'patient_identifier': convert_identifier})
    log.debug(f'Exam data altered!')
    return updated_exam, 200


@api.delete('/exams/<string:id>')
@api_auth(roles=['doctor'])
def exclude_exam(exam_id):
    log.info(f'Deleting exam {exam_id}.')
    exam = Exams.query.filter_by(id=exam_id).first_or_404()
    exam.delete()
    log.info("Exam deleted!")
    return jsonify({'Status': 'Deleted!'}), 200

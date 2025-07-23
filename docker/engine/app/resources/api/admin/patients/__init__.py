from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.patients import Patients
from flask import request, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.utils.converters.convert_user_datas import convert_identifier, convert_role_to_model
from engine.app.schemas.patients import PatientSchema, PatientUpdateSchema
from engine.app.config.logs import prepare_logs
from engine.app.utils.queries.build_query import build_query, dict_query

log = prepare_logs(__name__)


@api.get('/patients')
@api_auth(roles=['administrator'])
def list_patients():
    log.info('Retrieving patients.')
    patients = dict_query(build_query(Patients, with_entities=True).all(), True)
    log.debug(f'Returning patients: {len(patients)}')
    return jsonify({'Patients': patients}), 200


@api.post('/patients')
@api_auth(roles=['administrator'])
def add_user():
    log.info('Creating a new user.')
    data = request.json
    user = convert_json_to_model(Patients(), PatientSchema(), data, converters={'identifier': convert_identifier,
                                                                                'roles': convert_role_to_model})
    log.debug(f'User created: {user}')
    return user, 201


@api.put('/patients/<string:identifier>')
@api_auth(roles=['administrator'])
def edit_user(identifier):
    log.info(f'Altering data for user with identifier: {identifier}.')
    patient = Patients.query.filter_by(identifier=identifier).first_or_404()
    data = request.json
    updated_user = convert_json_to_model(patient, PatientUpdateSchema(), data,
                                         converters={'identifier': convert_identifier, 'roles': convert_role_to_model})
    log.debug(f'User data altered!')
    return updated_user, 200


@api.delete('/patients/<string:identifier>')
@api_auth(roles=['administrator'])
def delete_user(identifier):
    log.info(f'Deleting user {identifier}.')
    patient = Patients.query.filter_by(identifier=identifier).first_or_404()
    log.debug(f'Deleting user with ID: {patient.id}')
    patient.delete()
    log.info("User deleted!")
    return jsonify({'Status': 'Deleted!'}), 200

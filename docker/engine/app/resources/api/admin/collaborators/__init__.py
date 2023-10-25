from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.collaborators import Collaborators
from flask import request, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.utils.converters.convert_user_datas import convert_identifier, convert_role_to_model
from engine.app.schemas.collaborators.collaborator_schema import CollaboratorSchema, CollaboratorUpdateSchema
from engine.app.utils.generators.code_generator import generate_code
import logging

log = logging.getLogger("Higia." + __name__)


@api.get('/collaborators')
@api_auth(roles=['administrator'])
def list_collaborators():
    log.info('Retrieving patients.')
    collaborators = Collaborators.query.all()
    log.debug(f'Returning patients: {collaborators}')
    return jsonify({'Collaborators': [x.serialized(x.protected_fields) for x in collaborators]}), 200


@api.post('/collaborators')
@api_auth(roles=['administrator'])
def register_collaborator():
    log.info('Creating a new user.')
    data = request.json
    data['code'] = generate_code(12)
    collaborator = convert_json_to_model(Collaborators(), CollaboratorSchema(), data,
                                         converters={'identifier': convert_identifier, 'roles': convert_role_to_model})
    collaborator['code'] = data.get('code')
    log.debug(f'Collaborator created: {collaborator}')
    return collaborator, 201


@api.put('/collaborators/<string:code>')
@api_auth(roles=['administrator'])
def edit_collaborator(code):
    log.info(f'Altering data for collaborator with code: {code}.')
    collaborator = Collaborators.query.filter_by(code=code).first_or_404()
    data = request.json
    updated_user = convert_json_to_model(collaborator, CollaboratorUpdateSchema(), data,
                                         converters={'identifier': convert_identifier, 'roles': convert_role_to_model})
    log.debug(f'Collaborator data altered!')
    return updated_user, 200


@api.delete('/collaborators/<string:code>')
@api_auth(roles=['administrator'])
def delete_collaborator(code):
    log.info(f'Deleting collaborator with code: {code}.')
    collaborator = Collaborators.query.filter_by(code=code).first_or_404()
    log.debug(f'Deleting collaborator with ID: {collaborator.id}')
    collaborator.delete()
    log.info("Collaborator deleted!")
    return jsonify({'Status': 'Deleted!'}), 200

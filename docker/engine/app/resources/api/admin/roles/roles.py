from engine.app.resources.api import api
from engine.app.services.authentication import api_auth
from engine.app.models.intern.roles import Roles
from flask import request, abort, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.schemas.roles.roles_schema import RoleSchema
import logging

log = logging.getLogger("Higia." + __name__)


@api.route('/roles', methods=['GET'])
@api_auth(roles=['administrator'])
def list_roles():
    log.info('Retrieving roles.')
    roles = Roles.query.all()
    log.debug(f'Returning roles: {roles}')
    return jsonify({'Roles': [x.serialized for x in roles]}), 200


@api.route('/roles', methods=['POST'])
@api_auth(roles=['administrator'])
def add_role():
    log.info('Creating a new role.')
    data = request.json
    role = convert_json_to_model(Roles(), RoleSchema(), data)
    log.debug(f'Role created: {role["role_name"]}')
    return jsonify({'RoleID': role['id']}), 201


@api.route('/roles/<string:role_name>', methods=['DELETE'])
@api_auth(roles=['administrator'])
def delete_role(role_name):
    log.info(f'Deleting role {role_name}.')
    role = Roles.query.filter_by(role_name=role_name).first_or_404()
    log.debug(f'Deleting role with ID: {role.id}')
    role.delete()
    log.info("Role deleted!")
    return jsonify({'Status': 'Deleted!'}), 200

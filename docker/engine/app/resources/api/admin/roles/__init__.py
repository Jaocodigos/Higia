from engine.app.resources.api import api
from engine.app.services.authentication.auth_decorators import api_auth
from engine.app.models.intern.roles import Roles
from flask import request, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.schemas.roles.roles_schema import RoleSchema
from engine.app.config.logs import prepare_logs
from engine.app.utils.queries.build_query import build_query, dict_query

log = prepare_logs(__name__)


@api.get('/roles')
@api_auth(roles=['administrator'])
def list_roles():
    log.info('Retrieving roles.')
    roles = dict_query(build_query(Roles).all())
    log.debug(f'Returning roles: {len(roles)}')
    return jsonify({'Roles': roles}), 200


@api.post('/roles')
@api_auth(roles=['administrator'])
def add_role():
    log.info('Creating a new role.')
    data = request.json
    role = convert_json_to_model(Roles(), RoleSchema(), data)
    log.debug(f'Role created: {role["role_name"]}')
    return jsonify({'RoleID': role['id']}), 201


@api.delete('/roles/<string:role_name>')
@api_auth(roles=['administrator'])
def delete_role(role_name):
    log.info(f'Deleting role {role_name}.')
    role = Roles.query.filter_by(role_name=role_name).first_or_404()
    log.debug(f'Deleting role with ID: {role.id}')
    role.delete()
    log.info("Role deleted!")
    return jsonify({'Status': 'Deleted!'}), 200

from engine.app.resources.api import api
from engine.app.services.authentication import api_auth
from engine.app.models.intern.users import Users
from flask import request, abort, jsonify
from engine.app.utils.converters.convert_data_to_model import convert_json_to_model
from engine.app.utils.converters.convert_user_datas import convert_identifier
from engine.app.schemas.users.user_schema import UserSchema, UserUpdateSchema
import logging

log = logging.getLogger("Higia." + __name__)


@api.route('/users', methods=['GET'])
@api_auth(roles=['administrator'])
def list_users():
    log.info('Retrieving users.')
    users = Users.query.all()
    log.debug(f'Returning users: {users}')
    return jsonify({'Users': [x.serialized for x in users]}), 200


@api.route('/users', methods=['POST'])
@api_auth(roles=['administrator'])
def add_user():
    log.info('Creating a new user.')
    data = request.json
    user = convert_json_to_model(Users(), UserSchema(), data, converters={'identifier': convert_identifier})
    log.debug(f'User created: {user["name"]}')
    return user, 201


@api.route('/users/<string:identifier>', methods=['PUT'])
@api_auth(roles=['administrator'])
def edit_user(identifier):
    log.info(f'Altering data for user with identifier: {identifier}.')
    user = Users.query.filter_by(identifier=identifier).first_or_404()
    data = request.json
    updated_user = convert_json_to_model(user, UserUpdateSchema(), data)
    log.debug(f'User data altered!')
    return updated_user, 200


@api.route('/users/<string:identifier>', methods=['DELETE'])
@api_auth(roles=['administrator'])
def delete_user(identifier):
    log.info(f'Deleting user {identifier}.')
    user = Users.query.filter_by(identifier=identifier).first_or_404()
    log.debug(f'Deleting user with ID: {user.id}')
    user.delete()
    log.info("User deleted!")
    return jsonify({'Status': 'Deleted!'}), 200

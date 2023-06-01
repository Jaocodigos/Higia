from engine.app.resources.api import api
from engine.app.services.authentication import api_auth
from engine.app.models.intern.roles import Roles
from flask import request, abort, jsonify, logging

log = logging.getLogger("Higia." + __name__)


@api.route('/roles', methods=['GET'])
@api_auth(roles=['administrator'])
def list_roles():
    log.info('Retrieving roles.')
    roles = Roles.query.all()
    log.debug(f'Returning roles: {roles}')
    return jsonify({'Roles': roles}), 200

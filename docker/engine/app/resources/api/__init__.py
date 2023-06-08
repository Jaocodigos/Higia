from flask import Blueprint

api = Blueprint('api', import_name=__name__, url_prefix='/api')

#  TODO make a method to register routes without import all them
from engine.app.resources.api.admin.roles.roles import *
from engine.app.resources.api.med import *
from engine.app.resources.api.pacient import *

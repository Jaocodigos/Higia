from flask import Blueprint

api = Blueprint('api', import_name=__name__, url_prefix='/api')

from engine.app.resources.api.admin import *
from engine.app.resources.api.med import *
from engine.app.resources.api.pacient import *

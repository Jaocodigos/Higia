from flask import Blueprint

view = Blueprint('view', import_name=__name__, url_prefix='/')

from engine.app.resources.frontend.admin import *
from engine.app.resources.frontend.med import *
from engine.app.resources.frontend.pacient.login import *
from engine.app.resources.frontend.pacient.exams import *
from engine.app.resources.frontend.pacient.appointments import *
from engine.app.resources.frontend.users.profile import *

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from engine.app.models.intern.scheduling import Scheduling
from engine.app.models.intern.patients import Patients
from engine.app.models.intern.collaborators import Collaborators
from engine.app.models.intern.roles import Roles
from engine.app.models.intern.default import DefaultModel
from engine.app.models.intern.exams import Exams
from engine.app.models.intern.scheduling import DefaultModel


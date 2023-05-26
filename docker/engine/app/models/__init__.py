from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from engine.app.models.intern.users import Users
from engine.app.models.intern.roles import Roles
from engine.app.models.intern.default import DefaultModel


from engine.app.models import db
from .default import DefaultModel


class Roles(DefaultModel, db.Model):
    __tablename__ = 'roles'

    role_name = db.Column(db.String(50), unique=True, nullable=False)

    @property
    def protected_fields(self):
        return []

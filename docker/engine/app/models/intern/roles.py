from engine.app.models import db
from .default import DefaultModel
from engine.app.models.many_to_many import users_and_roles


class Roles(DefaultModel, db.Model):
    __tablename__ = 'roles'

    role_name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship("Users", secondary=users_and_roles, back_populates="roles", lazy="select")

    @property
    def protected_fields(self):
        return []

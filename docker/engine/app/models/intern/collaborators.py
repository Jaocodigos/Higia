from engine.app.models import db
from .default import DefaultModel
from .users import UsersModel
from engine.app.models.many_to_many import collaborators_and_roles


class Collaborators(DefaultModel, UsersModel, db.Model):
    __tablename__ = 'collaborators'

    code = db.Column(db.String(12), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    roles = db.relationship("Roles", secondary=collaborators_and_roles, back_populates="collaborators", lazy="select")
    doctor_exams = db.relationship('Exams', lazy='select', foreign_keys='Exams.doctor')
    doctor_schedulers = db.relationship('Scheduling', lazy='select', foreign_keys='Scheduling.doctor')

    @property
    def safe_fields(self):
        return 'id', 'full_name', 'locked'

    def check_roles(self, roles: list):
        if len(roles) > 0:
            for role in self.roles:
                if any(x == role.role_name for x in roles):
                    return True
        return False

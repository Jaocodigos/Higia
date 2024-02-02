from engine.app.models import db
from .default import DefaultModel
from .users import UsersModel
from engine.app.models.many_to_many import patients_and_roles


class Patients(DefaultModel, UsersModel, db.Model):
    __tablename__ = 'patients'

    identifier = db.Column(db.String(11), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(13), unique=True)
    cep = db.Column(db.String(255))
    roles = db.relationship("Roles", secondary=patients_and_roles, back_populates="patients", lazy="select")
    patient_exams = db.relationship('Exams', lazy='select', foreign_keys='Exams.patient')
    patient_schedulers = db.relationship('Scheduling', lazy='select', foreign_keys='Scheduling.patient')

    @property
    def safe_fields(self):
        return 'full_name', 'identifier', 'email', 'locked'

    def check_roles(self, roles: list):
        if len(roles) > 0:
            for role in self.roles:
                if any(x == role.role_name for x in roles):
                    return True
        return False

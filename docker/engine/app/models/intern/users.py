from engine.app.models import db
from .default import DefaultModel
from datetime import datetime
from engine.app.models.many_to_many import users_and_roles
from werkzeug.security import generate_password_hash, check_password_hash


class Users(DefaultModel, db.Model):
    __tablename__ = 'users'

    identifier = db.Column(db.String(11), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(500))
    phone = db.Column(db.String(13), unique=True)
    cep = db.Column(db.String(255))
    last_login = db.Column(db.DateTime, default=datetime.now())
    last_password_change = db.Column(db.DateTime)
    locked = db.Column(db.Boolean, default=False)
    blocked_until = db.Column(db.DateTime)
    login_tries = db.Column(db.Integer, default=0)
    roles = db.relationship("Roles", secondary=users_and_roles, back_populates="users", lazy="select")
    patient_exams = db.relationship('Exams', lazy='select', foreign_keys='Exams.patient')
    doctor_exams = db.relationship('Exams', lazy='select', foreign_keys='Exams.doctor')
    patient_schedulers = db.relationship('Scheduling', lazy='select', foreign_keys='Scheduling.patient')
    doctor_schedulers = db.relationship('Scheduling', lazy='select', foreign_keys='Scheduling.doctor')

    @property
    def protected_fields(self):
        return ['password_hash', 'cep', 'last_login', 'last_password_change', 'patient_exams', 'login_tries'
                'doctor_exams', 'patient_schedulers', 'doctor_schedulers', 'blocked_until']

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password_data):
        self.password_hash = generate_password_hash(password_data)

    def check_authorization(self, password):
        if check_password_hash(self.password_hash, password):
            return True
        return False

    def check_roles(self, roles: list):
        if len(roles) > 0:
            for role in self.roles:
                if any(x == role.role_name for x in roles):
                    return True
        return False

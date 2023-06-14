from engine.app.models import db
from .default import DefaultModel
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Users(DefaultModel, db.Model):
    __tablename__ = 'users'

    identifier = db.Column(db.String(11), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(500))
    phone = db.Column(db.String(13), unique=True)
    cep = db.Column(db.String(255))
    last_login = db.Column(db.DateTime, default=datetime.now())
    last_password_change = db.Column(db.DateTime)
    locked = db.Column(db.Boolean, default=False)
    blocked_until = db.Column(db.DateTime)
    login_tries = db.Column(db.Integer, default=0)
    roles = db.Column(db.Text(20000), default='users')

    @property
    def serialized(self):
        return dict(

            name=f"{self.first_name} {self.last_name}",
            cpf=self.identifier,
            email=self.email,
            phone=self.phone,
            is_locked=self.locked,
            roles=self.roles
        )

    def set_hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_authorization(self, password):
        if check_password_hash(self.password, password):
            return True
        return False

    def check_roles(self, roles: list):
        if len(roles) > 0 and any(x in roles for x in self.roles):
            return True
        return False

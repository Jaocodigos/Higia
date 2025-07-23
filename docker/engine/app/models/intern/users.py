
from engine.app.models import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class UsersModel(object):

    password_hash = db.Column(db.String(500))
    last_login = db.Column(db.DateTime, default=datetime.now())
    last_password_change = db.Column(db.DateTime)
    locked = db.Column(db.Boolean, default=False)
    blocked_until = db.Column(db.DateTime)
    login_tries = db.Column(db.Integer, default=0)

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


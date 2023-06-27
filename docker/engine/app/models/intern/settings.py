from engine.app.models import db
from .default import DefaultModel


class Settings(DefaultModel, db.Model):
    __tablename__ = 'settings'

    password_length = db.Column(db.Integer(), unique=False, default=0)
    password_numbers = db.Column(db.Integer(), unique=False, default=0)
    password_letters = db.Column(db.Integer(), unique=False, default=0)
    password_caps = db.Column(db.Integer(), unique=False, default=0)
    password_lower = db.Column(db.Integer(), unique=False, default=0)
    password_special = db.Column(db.Integer(), unique=False, default=0)
    log_level = db.Column(db.String(100), default='INFO')
    lockout = db.Column(db.Boolean(), default=False)
    lockout_tries = db.Column(db.Integer(), default=3)
    lockout_time = db.Column(db.Integer(), nullable=False, default=1)

    @property
    def serialized(self):
        return dict(
            password_length=self.password_length,
            password_numbers=self.password_numbers,
            password_letters=self.password_letters,
            password_high_chars=self.password_caps,
            password_lower_chars=self.password_lower,
            password_special=self.password_special,
            log_level=self.log_level,
            lockout_mode=self.lockout,
            lockout_tries=self.lockout_tries,
            lockout_time=self.lockout_time
        )


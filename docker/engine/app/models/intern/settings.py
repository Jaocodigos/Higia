from engine.app.models import db
from .default import DefaultModel


class Settings(DefaultModel, db.Model):
    __tablename__ = 'settings'

    password_length = db.Column(db.Integer(), unique=True, default=0)
    password_numbers = db.Column(db.Integer(), unique=True, default=0)
    password_letters = db.Column(db.Integer(), unique=True, default=0)
    password_caps = db.Column(db.Integer(), unique=True, default=0)
    password_lower = db.Column(db.Integer(), unique=True, default=0)
    password_special = db.Column(db.Integer(), unique=True, default=0)

    @property
    def serialized(self):
        return dict(
            id=self.id,
            numbers=self.password_numbers,
            letters=self.password_letters,
            high_chars=self.password_caps,
            lower_chars=self.password_lower,
            special=self.password_special
        )


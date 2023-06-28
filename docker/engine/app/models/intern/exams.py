from engine.app.models import db
from .default import DefaultModel


class Exams(DefaultModel, db.Model):
    __tablename__ = 'exams'

    result = db.Column(db.Text(), nullable=False)
    exam_type = db.Column(db.String(100), nullable=False)
    validity = db.Column(db.DateTime, nullable=False)
    patient = db.Column(db.String(50), db.ForeignKey("users.id"))
    doctor = db.Column(db.String(50), db.ForeignKey("users.id"))

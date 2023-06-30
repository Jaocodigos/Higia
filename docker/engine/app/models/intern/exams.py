from engine.app.models import db
from .default import DefaultModel


class Exams(DefaultModel, db.Model):
    __tablename__ = 'exams'

    result = db.Column(db.Text(), nullable=True)
    exam_type = db.Column(db.String(100), nullable=False)
    exam_local = db.Column(db.String(100), nullable=False)
    exam_date = db.Column(db.DateTime, nullable=False)
    validity = db.Column(db.DateTime, nullable=True)
    patient = db.Column(db.String(50), db.ForeignKey("users.id"))
    doctor = db.Column(db.String(50), db.ForeignKey("users.id"))

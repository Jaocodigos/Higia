from engine.app.models import db
from .default import DefaultModel


class Exams(DefaultModel, db.Model):
    __tablename__ = 'exams'

    result = db.Column(db.Text(), nullable=True)
    exam_type = db.Column(db.String(100), nullable=False)
    exam_local = db.Column(db.String(100), nullable=False)
    exam_date = db.Column(db.DateTime, nullable=False)
    validity = db.Column(db.DateTime, nullable=True)
    patient = db.Column(db.String(50), db.ForeignKey("patients.id"))
    patient_name = db.Column(db.String(100), nullable=False)
    patient_identifier = db.Column(db.String(11), nullable=False)
    doctor = db.Column(db.String(50), db.ForeignKey("collaborators.id"))
    doctor_name = db.Column(db.String(100), nullable=False)

    @property
    def protected_fields(self):
        return ['doctor', 'patient']

    @property
    def exam_date_formatted(self):
        return self.exam_date.strftime("%d/%m/%Y, %H:%M:%S")

    @property
    def validity_date_formatted(self):
        return self.exam_date.strftime("%d/%m/%Y, %H:%M:%S")

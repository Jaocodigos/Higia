from engine.app.models import db
from .default import DefaultModel


class Scheduling(DefaultModel, db.Model):
    __tablename__ = 'scheduling'

    description = db.Column(db.Text(), nullable=True)
    local = db.Column(db.Text(), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    appointment_day = db.Column(db.DateTime, nullable=False)
    details = db.Column(db.Text(), nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    patient = db.Column(db.String(50), db.ForeignKey("users.id"))
    patient_name = db.Column(db.String(100), nullable=False)
    patient_identifier = db.Column(db.String(11), nullable=False)
    doctor = db.Column(db.String(50), db.ForeignKey("users.id"))
    doctor_name = db.Column(db.String(100), nullable=False)

    @property
    def protected_fields(self):
        return ['doctor', 'patient']

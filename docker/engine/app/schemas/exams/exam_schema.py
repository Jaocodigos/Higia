from flask_marshmallow import Schema
from marshmallow import validates_schema, ValidationError
from engine.app.models.intern.exams import Exams
from engine.app.models.intern.users import Users
from engine.app.schemas.types import Types
from engine.app.utils.validators.identifier_validator import validate_identifier
import logging

log = logging.getLogger("Higia." + __name__)


class ExamSchema(Schema):
    class Meta:
        model = Exams

    patient_identifier = Types.String(required=True)
    exam_type = Types.String(required=True)
    exam_local = Types.String(required=True)
    exam_date = Types.Date(required=True)
    patient = Types.String(required=True)
    patient_name = Types.String(required=True)
    doctor = Types.String(required=True)
    doctor_name = Types.String(required=True)
    validity = Types.Date(required=True)
    result = Types.String()

    @validates_schema
    def validate_data(self, data, **kwargs):
        if not data.get('patient_identifier') or not validate_identifier(data.get('patient_identifier')):
            log.error("The identifier format is incorrect.")
            raise ValidationError("Invalid identifier, the correct format must contain 11 numbers.")


class ExamUpdateSchema(Schema):
    class Meta:
        model = Users

    patient_identifier = Types.String()
    exam_type = Types.String()
    exam_local = Types.String()
    exam_date = Types.String()
    validity = Types.String()
    result = Types.String()

    @validates_schema
    def validate_data(self, data, **kwargs):
        if not data.get('patient_identifier') or validate_identifier(data.get('patient_identifier')):
            log.error("The identifier format is incorrect.")
            raise ValidationError("Invalid identifier format, the correct format must contain 11 chars.")


from flask_marshmallow import Schema
from marshmallow import validates_schema, ValidationError
from engine.app.models.intern.exams import Exams
from engine.app.schemas.types import Types
from engine.app.utils.validators.identifier_validator import validate_identifier
from engine.app.utils.validators.date_validator import validate_date
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


class ExamSchema(Schema):
    class Meta:
        model = Exams

    patient_identifier = Types.String(required=True)
    exam_type = Types.String(required=True)
    exam_local = Types.String(required=True)
    exam_date = Types.String(required=True)
    patient = Types.String(required=True)
    patient_name = Types.String(required=True)
    doctor = Types.String(required=True)
    doctor_name = Types.String(required=True)
    validity = Types.String(required=True)
    result = Types.String()

    @validates_schema
    def validate_data(self, data, **kwargs):
        if not validate_identifier(data.get('patient_identifier')):
            log.error("The identifier format is incorrect.")
            raise ValidationError("Invalid identifier, the correct format must contain 11 numbers.")
        if not validate_date(data.get('exam_date')) or not validate_date(data.get('validity')):
            log.error("Invalid date format.")
            raise ValidationError("Invalid date format, please follow the instruction model.")


class ExamUpdateSchema(Schema):
    class Meta:
        model = Exams

    patient_identifier = Types.String()
    exam_type = Types.String()
    exam_local = Types.String()
    exam_date = Types.String()
    validity = Types.String()
    result = Types.String()

    @validates_schema
    def validate_data(self, data, **kwargs):
        if data.get('patient_identifier') and validate_identifier(data.get('patient_identifier')):
            log.error("The identifier format is incorrect.")
            raise ValidationError("Invalid identifier format, the correct format must contain 11 chars.")
        if data.get('exam_date') and not validate_date(data.get('exam_date')):
            log.error("Invalid date format.")
            raise ValidationError("Invalid exam date format, please follow the instruction model.")
        if data.get('validity') and not validate_date(data.get('exam_date')):
            log.error("Invalid date format.")
            raise ValidationError("Invalid validity date format, please follow the instruction model.")

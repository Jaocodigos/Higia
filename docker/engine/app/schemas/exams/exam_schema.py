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
    exam_date = Types.String(required=True)
    validity = Types.String(required=True)
    result = Types.String()

    @validates_schema
    def validate_data(self, data, **kwargs):
        if Users.query.filter_by(identifier=data.get('identifier')).first():
            log.error("This identifier is already in use.")
            raise ValidationError("This identifier is already in use.")
        if len(data.get('identifier')) > 11 or not data.get('identifier').isdigit():
            if not validate_identifier(data.get('identifier')):
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
        if data.get('identifier') and Users.query.filter_by(identifier=data.get('identifier')).first():
            log.error("This identifier is already in use.")
            raise ValidationError("This identifier is already in use.")
        if data.get('identifier') and (len(data.get('identifier')) > 11 or not data.get('identifier').isdigit()):
            log.error("The identifier format is incorrect.")
            raise ValidationError("Invalid identifier format, the correct format must contain 11 chars.")


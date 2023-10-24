from flask_marshmallow import Schema
from marshmallow import validates_schema, ValidationError
from engine.app.models.intern.scheduling import Scheduling
from engine.app.models.intern.users import Users
from engine.app.schemas.types import Types
from engine.app.utils.validators.identifier_validator import validate_identifier
from engine.app.utils.validators.date_validator import validate_date
import logging

log = logging.getLogger("Higia." + __name__)


class ScheduleSchema(Schema):
    class Meta:
        model = Scheduling

    local = Types.String(required=True)
    patient = Types.String(required=True)
    patient_name = Types.String(required=True)
    patient_identifier = Types.String(required=True)
    doctor = Types.String(required=True)
    doctor_name = Types.String(required=True)
    appointment_day = Types.String(required=True)
    return_date = Types.String()
    description = Types.String()
    specialty = Types.String(required=True)
    details = Types.String()

    @validates_schema
    def validate_data(self, data, **kwargs):
        if data.get('patient_identifier') and not validate_identifier(data.get('patient_identifier')):
            log.error("The identifier format is incorrect.")
            raise ValidationError("Invalid identifier format, the correct format must contain 11 chars.")
        if not validate_date(data.get('appointment_day')):
            log.error("Invalid date format.")
            raise ValidationError("Invalid exam date format, please follow the instruction model.")


class ScheduleUpdateSchema(Schema):
    class Meta:
        model = Scheduling

    local = Types.String()
    appointment_day = Types.String()
    return_date = Types.String()
    description = Types.String()
    specialty = Types.String()
    details = Types.String()

    @validates_schema
    def validate_data(self, data, **kwargs):
        if data.get('appointment_day') and not validate_date(data.get('appointment_day')):
            log.error("Invalid date format.")
            raise ValidationError("Invalid exam date format, please follow the instruction model.")
        if data.get('return_date') and not validate_date(data.get('return_date')):
            log.error("Invalid date format.")
            raise ValidationError("Invalid validity date format, please follow the instruction model.")

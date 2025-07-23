from flask_marshmallow import Schema
from marshmallow import validates_schema, ValidationError
from engine.app.models.intern.patients import Patients
from engine.app.models.intern.roles import Roles
from engine.app.schemas.types import Types
from engine.app.utils.validators.password_validator import validate_password_policy
from engine.app.utils.validators.identifier_validator import validate_identifier
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


class PatientSchema(Schema):
    class Meta:
        model = Patients

    identifier = Types.String(required=True)
    email = Types.String(required=True)
    full_name = Types.String(required=True)
    password = Types.String(required=True)
    phone = Types.String()
    cep = Types.String()
    roles = Types.List(Types.String())

    @validates_schema
    def validate_data(self, data, **kwargs):
        if Patients.query.filter_by(identifier=data.get('identifier')).first():
            log.error("This identifier is already in use.")
            raise ValidationError("This identifier is already in use.")
        if not data.get('identifier') or not validate_identifier(data.get('identifier')):
            log.error("The identifier format is missing or is incorrect.")
            raise ValidationError("Invalid identifier, the correct format must contain 11 numbers.")
        if '.com' not in data.get('email') or '@' not in data.get('email'):
            log.error("Invalid email.")
            raise ValidationError("Invalid email.")
        if not validate_password_policy(data.get('password')):
            log.error("Invalid password.")
            raise ValidationError("Invalid password, follow the current policy.")
        if data.get('phone') and not data.get('phone').isdigit():
            log.error("Invalid phone")
            raise ValidationError("Invalid phone.")
        if data.get('role') and not Roles.query.filter_by(role_name=data.get('role')).first():
            log.error(f"The role {data.get('role')} doesn't exist.")
            raise ValidationError("The inserted role doesn't exist.")


class PatientUpdateSchema(Schema):
    class Meta:
        model = Patients

    identifier = Types.String()
    email = Types.String()
    full_name = Types.String()
    password = Types.String()
    phone = Types.String()
    cep = Types.String()
    roles = Types.List(Types.String())

    @validates_schema
    def validate_data(self, data, **kwargs):
        if data.get('identifier') and Patients.query.filter_by(identifier=data.get('identifier')).first():
            log.error("This identifier is already in use.")
            raise ValidationError("This identifier is already in use.")
        if data.get('identifier') and not validate_identifier(data.get('identifier')):
            log.error("The identifier format is incorrect.")
            raise ValidationError("Invalid identifier format, the correct format must contain 11 chars.")
        if data.get('email') and '.com' not in data.get('email') or data.get('email') and '@' not in data.get('email'):
            log.error("Invalid email.")
            raise ValidationError("Invalid email.")
        if data.get('password') and not validate_password_policy(data.get('password')):
            log.error("Invalid password.")
            raise ValidationError("Invalid password, follow the current policy.")
        if data.get('phone') and not data.get('phone').isdigit():
            log.error("Invalid phone")
            raise ValidationError("Invalid phone.")
        if data.get('role') and not Roles.query.filter_by(role_name=data.get('role')).first():
            log.error(f"The role {data.get('role')} doesn't exist.")
            raise ValidationError("The inserted role doesn't exist.")


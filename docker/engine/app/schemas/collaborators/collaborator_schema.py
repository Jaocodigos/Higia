from flask_marshmallow import Schema
from marshmallow import validates_schema, ValidationError
from engine.app.models.intern.collaborators import Collaborators
from engine.app.models.intern.roles import Roles
from engine.app.schemas.types import Types
from engine.app.utils.validators.password_validator import validate_password_policy
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


class CollaboratorSchema(Schema):
    class Meta:
        model = Collaborators

    full_name = Types.String(required=True)
    code = Types.String(required=True)
    password = Types.String(required=True)
    roles = Types.List(Types.String(), default='nurse')

    @validates_schema
    def validate_data(self, data, **kwargs):
        if not validate_password_policy(data.get('password')):
            log.error("Invalid password.")
            raise ValidationError("Invalid password, follow the current policy.")
        if data.get('role') and not Roles.query.filter_by(role_name=data.get('role')).first():
            log.error(f"The role {data.get('role')} doesn't exist.")
            raise ValidationError("The inserted role doesn't exist.")


class CollaboratorUpdateSchema(Schema):
    class Meta:
        model = Collaborators

    full_name = Types.String()
    password = Types.String()
    roles = Types.List(Types.String())

    @validates_schema
    def validate_data(self, data, **kwargs):
        if data.get('password') and not validate_password_policy(data.get('password')):
            log.error("Invalid password.")
            raise ValidationError("Invalid password, follow the current policy.")
        if data.get('role') and not Roles.query.filter_by(role_name=data.get('role')).first():
            log.error(f"The role {data.get('role')} doesn't exist.")
            raise ValidationError("The inserted role doesn't exist.")


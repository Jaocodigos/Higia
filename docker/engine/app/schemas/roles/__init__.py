
from flask_marshmallow import Schema
from marshmallow import validates_schema, ValidationError
from engine.app.models.intern.roles import Roles
from engine.app.schemas.types import Types
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


class RoleSchema(Schema):
    class Meta:
        model = Roles

    role_name = Types.String(required=True)

    @validates_schema
    def validate_data(self, data, **kwargs):
        if Roles.query.filter_by(role_name=data.get('role_name')).first():
            log.warning("This Role already exist.")
            raise ValidationError("This Role already exist.")


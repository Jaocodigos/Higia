from engine.app.schemas import ma
from engine.app.models.intern.roles import Roles
from engine.app.schemas.types import Types
from engine.app.utils.validators.name_validator import UniqueNameValidator


class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Roles

    name = Types.String(required=True, validate=UniqueNameValidator())

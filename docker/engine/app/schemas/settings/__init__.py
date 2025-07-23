from flask_marshmallow import Schema
from marshmallow import validates_schema, ValidationError
from engine.app.models.intern.settings import Settings
from engine.app.schemas.types import Types
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)

log_types = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


class SettingsSchema(Schema):
    class Meta:
        model = Settings

    password_length = Types.Integer()
    password_numbers = Types.Integer()
    password_letters = Types.Integer()
    password_caps = Types.Integer()
    password_lower = Types.Integer()
    password_special = Types.Integer()
    log_level = Types.String()
    lockout = Types.Boolean()
    lockout_tries = Types.Integer()
    lockout_time = Types.Integer()

    @validates_schema
    def validate_data(self, data, **kwargs):
        if data.get('log_level') and data.get('log_level') not in log_types:
            log.error(f'Invalid log type inserted: {data.get("log_level")}')
            raise ValidationError('Invalid log type.')

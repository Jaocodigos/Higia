from engine.app.models.intern.settings import Settings
from engine.app.models import db


def set_default_db_config():
    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        settings.password_letters = 6
        settings.password_length = 6
        settings.save()

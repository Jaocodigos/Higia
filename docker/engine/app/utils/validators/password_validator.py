from engine.app.models.intern.settings import Settings
from engine.app.config.default import set_default_db_config
import logging

log = logging.getLogger("Higia." + __name__)


def validate_password_policy(password):
    log.debug(f"Validating password {password}")
    set_default_db_config()
    settings = Settings.query.first()
    if len(password) > settings.password_length:
        return False
    letters = 0
    numbers = 0
    lower = 0
    high = 0
    special = 0
    for c in password:
        if c.isalpha():
            letters += 1
            if c.isupper():
                high += 1
            elif c.islower():
                lower += 1
        elif c.isdigit():
            numbers += 1
        elif c.isalnum():
            special += 1
    if numbers < settings.password_numbers:
        return False
    if letters < settings.password_letters:
        return False
    if lower < settings.password_lower:
        return False
    if high < settings.password_caps:
        return False
    if special < settings.password_special:
        return False
    return True
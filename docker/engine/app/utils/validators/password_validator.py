from engine.app.config.default import set_default_db_config
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


def validate_password_policy(password):
    log.debug(f"Validating password {password}")
    settings = set_default_db_config()
    if len(password) > settings.password_length:
        log.error(f"The password must contain at less {settings.password_length} chars.")
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
        log.error(f"The password must contain at less {settings.password_numbers} numbers.")
        return False
    if letters < settings.password_letters:
        log.error(f"The password must contain at less {settings.password_letters} letters.")
        return False
    if lower < settings.password_lower:
        log.error(f"The password must contain at less {settings.password_lower} lower chars.")
        return False
    if high < settings.password_caps:
        log.error(f"The password must contain at less {settings.password_caps} high chars.")
        return False
    if special < settings.password_special:
        log.error(f"The password must contain at less {settings.password_special} special chars.")
        return False
    return True

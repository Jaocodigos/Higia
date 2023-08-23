from engine.app.models.intern.users import Users
from engine.app.models.intern.settings import Settings
from datetime import datetime, timedelta
import logging

log = logging.getLogger("Higia." + __name__)


def validate_login(user: Users, **kwargs):
    settings = Settings.query.first()
    if not user.check_authorization(kwargs.get('password')):
        log.debug(f"Invalid password. Verifying user login tries.")
        if user.login_tries >= settings.lockout_tries:
            log.debug("The user passed login tries limit. Blocking temporarily.")
            user.locked = True
            user.blocked_until = datetime.now() + timedelta(hours=settings.lockout_time)
            user.save()
        return False
    log.debug("Login validated! Resetting login tries.")
    user.login_tries = 0
    user.save()
    return True


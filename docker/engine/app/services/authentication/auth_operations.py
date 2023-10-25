from engine.app.models.intern.patients import Patients
from engine.app.models.intern.collaborators import Collaborators
from engine.app.utils.converters.convert_user_datas import convert_identifier
from engine.app.models.intern.settings import Settings
from datetime import datetime, timedelta
from os import environ
import logging

log = logging.getLogger("Higia." + __name__)


try:
    admin_username = environ['ADMIN_USERNAME']
except KeyError:
    exit("Missing ADMIN_USERNAME environment variable.")

try:
    admin_password = environ['ADMIN_PASSWORD']
except KeyError:
    exit("Missing ADMIN_PASSWORD environment variable.")


def validate_admin(auth):
    if admin_username == auth.username and admin_password == auth.password:
        log.debug(f"User {auth.username} is a valid administrator: True.")
        return True
    log.debug(f"User {auth.username} is a valid administrator: False.")
    return False


def validate_user_type(user_model):
    if user_model.__getattr__('code'):
        return {'code': user_model.code}
    else:
        return {'identifier': user_model.identifier}


def validate_login(**kwargs):
    settings = Settings.query.first()
    if convert_identifier(kwargs.get('identifier')):
        user = Patients.query.filter_by(identifier=kwargs.get('identifier')).first()
    else:
        user = Collaborators.query.filter_by(identifier=kwargs.get('identifier')).first()
    if not user:
        log.debug(f"User with identifier: {kwargs.get('identifier')} not found. Aborting operation.")
        return False, None
    if not user.check_authorization(kwargs.get('password')):
        log.debug(f"Invalid password. Verifying user login tries.")
        if user.login_tries >= settings.lockout_tries:
            log.debug("The user passed login tries limit. Blocking temporarily.")
            user.locked = True
            user.blocked_until = datetime.now() + timedelta(hours=settings.lockout_time)
            user.save()
        return False, None
    if kwargs.get('roles') and not user.check_roles(kwargs.get('roles')):
        log.debug("The role doesn't match with requested.")
        return False, None
    log.debug("Login validated! Resetting login tries.")
    user.login_tries = 0
    user.save()
    user_data = {'username': f'{user.full_name}'}
    user_data.update(validate_user_type(user))
    return True, user_data

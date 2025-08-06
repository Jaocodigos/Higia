from engine.app.models.intern.patients import Patients
from engine.app.models.intern.collaborators import Collaborators
from engine.app.utils.converters.convert_user_datas import convert_identifier
from engine.app.models.intern.settings import Settings
from datetime import datetime, timedelta
from os import environ
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


try:
    admin_username = environ['ADMIN_USERNAME']
except KeyError:
    exit("Missing ADMIN_USERNAME environment variable.")

try:
    admin_password = environ['ADMIN_PASSWORD']
except KeyError:
    exit("Missing ADMIN_PASSWORD environment variable.")


def validate_admin(auth, api_call=True) -> bool:
    if api_call:
        auth_username = auth.username
        auth_password = auth.password
    else:
        auth_username = auth.identifier.data
        auth_password = auth.password.data
    if admin_username == auth_username and admin_password == auth_password:
        log.debug(f"User '{auth_username}' is a valid administrator: True.")
        return True
    log.debug(f"User '{auth_username}' is a valid administrator: False.")
    return False


def validate_user_type(user_model):
    if 'code' in user_model.__dict__.keys():
        return {'code': user_model.code}
    else:
        return {'identifier': user_model.identifier}


def validate_login(**kwargs):
    settings = Settings.query.first()
    identifier = convert_identifier(kwargs.get('code_or_identifier'))
    if identifier:
        user = Patients.query.filter_by(identifier=identifier).first()
    else:
        user = Collaborators.query.filter_by(code=kwargs.get('code_or_identifier')).first()
    if not user:
        log.debug(f"User identified by '{kwargs.get('code_or_identifier')}' not found. Aborting operation.")
        return False, None
    if not kwargs.get("existent_session") and not user.check_authorization(kwargs.get('password')):
        log.debug(f"Invalid password. Verifying user '{kwargs.get('code_or_identifier')}' login tries.")
        if user.login_tries >= settings.lockout_tries:
            log.debug(f"User identified by '{kwargs.get('code_or_identifier')}' passed login tries limit. Blocking temporarily.")
            user.locked = True
            user.blocked_until = datetime.now() + timedelta(hours=settings.lockout_time)
            user.save()
        return False, None
    if kwargs.get('roles') and not user.check_roles(kwargs.get('roles')):
        log.debug(f"User identified by '{kwargs.get('code_or_identifier')}' role doesn't match with requested by operation.")
        return False, None
    log.debug("Login validated! Resetting login tries.")
    user.login_tries = 0
    user.save()
    user_data = {'username': f'{user.full_name}', 'roles': [x.role_name for x in user.roles]}
    user_data.update(validate_user_type(user))
    return True, user_data

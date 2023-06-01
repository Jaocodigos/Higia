from functools import wraps
from flask import request, abort, session
from os import environ
from engine.app.models.intern.users import Users
from engine.app.utils.converters.convert_user_datas import convert_identifier


try:
    admin_username = environ['ADMIN_USERNAME']
except KeyError:
    exit("Missing ADMIN_USERNAME environment variable.")

try:
    admin_password = environ['ADMIN_PASSWORD']
except KeyError:
    exit("Missing ADMIN_PASSWORD environment variable.")


def api_auth(roles=[]):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            auth = request.authorization
            if auth and hasattr(auth, 'username') and hasattr(auth, 'password'):
                if admin_username == auth.username and admin_password == auth.password:
                    return func(*args, **kwargs)
            if request.headers.get('identifier') and request.headers.get('password'):
                user_id = convert_identifier(request.args.get('identifier'))
                passwd = request.headers.get('password')
                user = Users.query.filter_by(identifier=user_id).first()
                if user and user.check_password(passwd):
                    if roles and user.check_roles(roles):
                        return func(*args, **kwargs)
                    if not roles:
                        return func(*args, **kwargs)
                    abort(401, "Unauthorized.")
            if 'client-id' in request.headers and 'client' in roles:
                ##  TODO authentication for client with api-key
                abort(401, "Unauthorized.")
            abort(401, "Unauthorized.")
        return wrap
    return decorator

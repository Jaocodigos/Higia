from functools import wraps
from flask import request, abort, session, redirect, url_for, flash
from engine.app.utils.converters.convert_user_datas import convert_identifier
from engine.app.services.authentication.auth_operations import validate_login, validate_admin
from engine.app.utils.base_classes.dummy_user import DummyUser


def api_auth(roles: list):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            auth = request.authorization
            if auth and hasattr(auth, 'username') and hasattr(auth, 'password'):
                if validate_admin(auth) and "administrator" in roles:
                    return func(*args, **kwargs)
                else:
                    validated, user_data = validate_login(code_or_identifier=auth.username,
                                                          password=auth.password, roles=roles)
                    if validated:
                        user = DummyUser(**user_data)
                        return func(user, *args, **kwargs)

                    abort(401, "Unauthorized.")
            if 'client-id' in request.headers and 'client' in roles:
                # TODO authentication for client with api-key
                abort(401, "Unauthorized.")
            abort(401, "Unauthorized.")
        return wrap
    return decorator

def login_required(roles: list):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            if session.get("user") :
                user_data = dict(username=session.get("user"), code=session.get("code"),
                                 identifier=session.get("identifier"))
                if session.get("role") in roles:
                    user = DummyUser(**user_data)
                    return func(user, *args, **kwargs)
                flash("You're not allowed to proceed with this operation.", "danger")
                return redirect("view.home")
            flash("Unauthorized, please authenticate again.", "danger")
            return redirect(url_for("view.login"))
        return wrap
    return decorator


from flask import render_template, flash, redirect, url_for

from engine.app.resources.frontend import view
from engine.app.resources.frontend.pacient.login.form import LoginForm
from engine.app.models.intern.patients import Patients
from engine.app.services.authentication.auth_operations import validate_login, validate_admin
from engine.app.services.authentication.session import create_session, erase_session
from engine.app.config.logs import prepare_logs
from engine.app.services.authentication.auth_decorators import check_login_route, login_required

log = prepare_logs(__name__)


@view.get('/')
@view.get('/home')
@login_required([])
def home():
    # This function os only for test template for now. This will change in the future.
    return render_template('restricted/dashboard.html')


@view.route('/login', methods=['GET', 'POST'])
@check_login_route()
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():

        log.debug(f"Login submitted by user: {login_form.identifier.data}")
        if validate_admin(login_form, False):

            log.debug("Administrator detected.")
            create_session("admin", "administrator", "000000", "00000000000")
            return redirect(url_for("view.home"))

        valid, user = validate_login(code_or_identifier=login_form.identifier.data, password=login_form.password.data)
        if valid:

            log.debug(f"Found user with identifier: '{login_form.identifier.data}', creating session.")
            create_session(user.get("username"), user.get("roles"), code=user.get("code", None), identifier=user.get("identifier", None))
            return redirect(url_for("view.home"))

        log.debug(f"User '{login_form.identifier.data}' is invalid.")
        flash("Invalid identifier or password.", "error")
        return render_template('layouts/login.html', form=login_form)

    return render_template('layouts/login.html', form=login_form)


@view.get('/logout')
@login_required([])
def logout():
    erase_session()
    return redirect(url_for("view.login"))


from flask import render_template, flash, redirect, url_for

from engine.app.resources.frontend import view
from engine.app.resources.frontend.pacient.login.form import LoginForm
from engine.app.models.intern.patients import Patients
from engine.app.services.authentication.auth_operations import validate_login, validate_admin
from engine.app.services.authentication.session import create_session
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


@view.route('/', methods=['GET', 'POST'])
def home():
    # This function os only for test template for now. This will change in the future.
    return render_template('restricted/dashboard.html')


@view.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        log.debug(f"Login submitted by user: {login_form.name.data}")
        if validate_admin(form):
            log.debug("Administrator detected.")
            create_session("admin", "administrator", "000000", "00000000000")
            return redirect(url_for("view.home"))
        patient = Patients.query.filter_by().first()
        log.debug(f"Found user: {patient.id}")
        if not patient or not validate_login(code_or_identifier=patient, password=login_form.password.data):
            log.debug(f"User {patient} is invalid.")
            flash("Invalid user or password.", "error")
            return render_template('login.html', form=login_form)
        return redirect(url_for("view.home"))
    return render_template('layouts/login.html', form=login_form)

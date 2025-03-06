from engine.app.resources.frontend import view
from flask import render_template, flash
from engine.app.resources.frontend.pacient.login.form import LoginForm
from engine.app.models.intern.patients import Patients
from engine.app.services.authentication.auth_operations import validate_login
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
        patient = Patients.query.filter_by().first()
        log.debug(f"Found user: {patient.id}")
        if not patient or not validate_login(code_or_identifier=patient, password=login_form.password.data):
            log.debug(f"User {patient} is invalid.")
            flash("Invalid user or password.", "error")
            return render_template('login.html', form=login_form)
    return render_template('layouts/login.html', form=login_form)

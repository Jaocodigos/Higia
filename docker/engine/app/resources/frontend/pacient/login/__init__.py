from engine.app.resources.frontend import view
from flask import render_template, redirect, url_for, flash
from engine.app.resources.frontend.pacient.login.form import LoginForm
from engine.app.models.intern.patients import Patients
from engine.app.services.authentication.auth_operations import validate_login
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


@view.route('/', methods=['GET', 'POST'])
@view.route('/login', methods=['GET', 'POST'])
def login():
    log.info("Higia Login-Page")
    login_form = LoginForm()
    if login_form.validate_on_submit():
        log.debug(f"Login submitted by user: {login_form.name.data}")
        patient = Patients.query.filter_by().first()
        log.debug(f"Found user: {patient.id}")
        if not patient or not validate_login(patient, password=login_form.password.data):
            log.debug(f"User {patient} is invalid.")
            flash("Invalid user or password.", "error")
            return redirect(url_for('view.login'))
    return render_template('login.html', form=login_form)

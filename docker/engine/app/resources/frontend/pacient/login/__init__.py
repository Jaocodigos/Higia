from engine.app.resources.frontend import view
from flask import render_template, redirect, url_for, flash
from engine.app.resources.frontend.pacient.login.form import LoginForm
from engine.app.models.intern.users import Users
from engine.app.services.authentication.auth_operations import validate_login
import logging

log = logging.getLogger("Higia." + __name__)


@view.route('/', methods=['GET', 'POST'])
@view.route('/login', methods=['GET', 'POST'])
def login():
    log.info("Higia Login-Page")
    login_form = LoginForm()
    if login_form.validate_on_submit():
        log.debug(f"Login submitted by user: {login_form.name.data}")
        user = Users.query.filter_by().first()
        log.debug(f"Found user: {user.id}")
        if not user or not validate_login(user, password=login_form.password.data):
            log.debug(f"User {user} is invalid.")
            flash("Invalid user or password.", "error")
            return redirect(url_for('view.login'))
    return render_template('login.html', form=login_form)

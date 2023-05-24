from engine.app.resources.frontend import view
from flask import session, render_template
import logging

log = logging.getLogger("Higia." + __name__)


@view.route('/', methods=['GET', 'POST'])
@view.route('/login', methods=['GET', 'POST'])
def login():
    log.info("Login-Page")
    return render_template('login.html')

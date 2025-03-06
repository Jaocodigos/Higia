from flask import render_template, flash, redirect, url_for

from engine.app.resources.frontend import view
from engine.app.resources.frontend.pacient.exams.form import ExamForm
from engine.app.config.logs import prepare_logs
from engine.app.models import db, Exams

log = prepare_logs(__name__)


@view.route('/exams', methods=['GET'])
def exams():
    exam_history = db.session.execute(db.select(Exams)).scalars()
    return render_template('restricted/exams/list.html', exams=exam_history)


@view.route('/exams/new', methods=['GET', 'POST'])
def register_exam():
    exam_form = ExamForm()
    if exam_form.validate_on_submit():
        flash('Exam scheduled!', 'success')
        return redirect(url_for('views.exams'))
    return render_template('restricted/exams/form.html', form=exam_form)

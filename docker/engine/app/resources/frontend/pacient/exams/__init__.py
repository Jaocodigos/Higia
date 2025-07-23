from flask import render_template, flash, redirect, url_for

from engine.app.resources.frontend import view
from engine.app.resources.frontend.pacient.exams.form import ExamForm
from engine.app.config.logs import prepare_logs
from engine.app.models import db, Exams, Collaborators
from engine.app.schemas.exams import ExamSchema
from engine.app.utils.converters import convert_json_to_model, form_to_json

log = prepare_logs(__name__)


@view.route('/exams', methods=['GET'])
def exams():
    scheduled_exams = db.session.execute(db.select(Exams)).scalars().all()
    if scheduled_exams:
        scheduled_exams = scheduled_exams.serialized()
    return render_template('restricted/exams/list.html', exams=scheduled_exams)


@view.route('/exams/new', methods=['GET', 'POST'])
def register_exam():
    doctors = db.session.execute(db.select(Collaborators)).scalars()
    exam_form = ExamForm(doctors)
    if exam_form.validate_on_submit():
        payload = form_to_json(exam_form)
        convert_json_to_model(Exams(), ExamSchema(), payload)
        flash('Exam scheduled!', 'success')
        return redirect(url_for('views.exams'))
    return render_template('restricted/exams/form.html', form=exam_form)

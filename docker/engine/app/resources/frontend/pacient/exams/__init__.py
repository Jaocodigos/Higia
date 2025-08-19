from flask import render_template, flash, redirect, url_for, session

from engine.app.resources.frontend import view
from engine.app.resources.frontend.pacient.exams.form import ExamForm
from engine.app.config.logs import prepare_logs
from engine.app.models import db, Exams, Patients, Collaborators
from engine.app.utils.converters.convert_user_datas import convert_identifier
from engine.app.utils.converters.convert_dates import convert_string_date_to_datetime
from engine.app.schemas.exams import ExamSchema
from engine.app.utils.converters import convert_json_to_model, form_to_json
from engine.app.services.authentication.auth_decorators import login_required

log = prepare_logs(__name__)


@view.get('/exams')
@login_required(['patient', 'doctor'])
def exams():
    scheduled_exams = db.session.execute(db.select(Exams)).scalars().all()
    if scheduled_exams:
        scheduled_exams = [x.convert_data_to_table() for x in scheduled_exams]

    return render_template('restricted/exams/list.html', exams=scheduled_exams)


@view.route('/exams/new', methods=['GET', 'POST'])
@login_required(['doctor'])
def register_exam():
    exam_form = ExamForm()
    if exam_form.validate_on_submit():

        exam_data = form_to_json(exam_form)

        doctor = db.session.execute(db.select(Collaborators).filter_by(code=session.get('code'))).scalar_one()
        patient = db.session.execute(db.select(Patients).filter_by(identifier=exam_data.get('patient_identifier'))).scalar_one()

        if not doctor:
            flash('Session expired, please log in again.', 'danger')
            return redirect(url_for('view.logout'))

        if not patient:
            flash('Invalid patient identifier, please review patient data and try again.', 'danger')
            return render_template('restricted/exams/form.html', form=exam_form)

        exam_data["patient"] = patient.id
        exam_data["patient_name"] = patient.full_name
        exam_data["doctor"] = doctor.id
        exam_data["doctor_name"] = doctor.full_name
        exam_data["exam_date"] = f'{exam_data.get("exam_date")}, {exam_data.get("exam_hour")}'

        # TODO: ADD DYNAMIC LOCAL
        exam_data["exam_local"] = 'U. DIADEMA - SP'

        convert_json_to_model(Exams(), ExamSchema(), exam_data, converters={'patient_identifier': convert_identifier,
                                                                            'exam_date': convert_string_date_to_datetime,
                                                                            'validity': convert_string_date_to_datetime})
        flash('Exam scheduled!', 'success')
        return redirect(url_for('view.exams'))

    return render_template('restricted/exams/form.html', form=exam_form)

from flask import render_template, flash, redirect, url_for, session

from engine.app.resources.frontend import view
from engine.app.resources.frontend.pacient.appointments.form import AppointmentForm
from engine.app.config.logs import prepare_logs
from engine.app.models import db, Scheduling, Collaborators, Exams, Patients
from engine.app.schemas.schedulers import ScheduleSchema
from engine.app.utils.converters import convert_json_to_model, form_to_json
from engine.app.services.authentication.auth_decorators import login_required
from engine.app.utils.converters.convert_dates import convert_string_date_to_datetime

log = prepare_logs(__name__)


@view.route('/appointments', methods=['GET'])
@login_required([])
def appointments():
    appoints = db.session.execute(db.select(Scheduling)).scalars().all()
    if appoints:
        appoints = [x.convert_data_to_table() for x in appoints]

    return render_template('restricted/appointments/list.html', appointments=appoints)


@view.route('/appointments/new', methods=['GET', 'POST'])
@login_required([])
def schedule_appointment():
    doctors = db.session.execute(db.select(Collaborators)).scalars()
    appointment_form = AppointmentForm(doctors)
    if appointment_form.validate_on_submit():

        doctor = appointment_form.doctor.data.split('|')
        patient = Patients.query.filter_by(identifier=session.get('identifier')).with_entities(Patients.id).first_or_404()
        appointment_data = form_to_json(appointment_form)

        appointment_data.update({
            'patient_identifier': session.get('identifier'),
            'patient_name': session.get('user'),
            'patient': patient.id,
            'doctor': doctor[0],
            'doctor_name': doctor[1],
            'local': 'U. Diadema - SP'
        })

        convert_json_to_model(Scheduling(), ScheduleSchema(), appointment_data,
                              converters={'appointment_day': convert_string_date_to_datetime})
        flash('Exam scheduled!', 'success')
        return redirect(url_for('views.appointments'))

    return render_template('restricted/exams/form.html', form=appointment_form)

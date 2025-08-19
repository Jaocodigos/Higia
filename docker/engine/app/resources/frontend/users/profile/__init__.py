from flask import flash, redirect, url_for, render_template, session

from engine.app.resources.frontend import view
from engine.app.resources.frontend.users.profile.form import ProfileForm
from engine.app.services.authentication.auth_decorators import login_required
from engine.app.models import db, Patients
from engine.app.utils.converters import form_to_json, convert_json_to_model
from engine.app.schemas.patients import PatientUpdateSchema
from engine.app.utils.converters.convert_user_datas import convert_identifier


@view.route('/profile', methods=['GET', 'POST'])
@login_required(['patient'])
def profile():
    patient = db.session.execute(db.select(Patients).filter_by(identifier=session.get('identifier'))).scalar_one()
    profile_form = ProfileForm()
    if profile_form.validate_on_submit():
        patient_data = form_to_json(profile_form)
        convert_json_to_model(patient, PatientUpdateSchema(), patient_data, converters={'patient_identifier': convert_identifier})
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('view.profile'))
    profile_form.identifier.data = patient.identifier
    profile_form.full_name.data = patient.full_name
    profile_form.email.data = patient.email
    profile_form.phone.data = patient.phone
    profile_form.cep.data = patient.cep
    return render_template('restricted/profile/form.html', form=profile_form)
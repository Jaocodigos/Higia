from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired


class AppointmentForm(FlaskForm):

    def __init__(self, doctors, *args, **kwargs):
        doctors = [(f'{x.id}|{x.full_name}', x.full_name) for x in doctors] if doctors else []
        self.doctor.kwargs['choices'] = doctors
        super(AppointmentForm, self).__init__(*args, **kwargs)

    specialty = SelectField('Specialty', choices=[("ophthalmologist", "Ophthalmologist"), ("cardiologist", "Cardiologist"),
                                                  ("otorhinologist", "Otorhinologist"), ("neurologist", "Neurologist"),
                                                  ("urologist", "Urologist"), ("physiotherapist", "Physiotherapist")], validators=[DataRequired()])
    doctor = SelectField('Doctor', choices=[], validators=[DataRequired()])
    appointment_day = DateField('Appointment Day', validators=[DataRequired()])
    # return_date = DateField('Returning On') This field must appear only for doctors

    description = TextAreaField('Description')
    # details = StringField('Details') This field must appear only for doctors

    submit = SubmitField('Confirm')

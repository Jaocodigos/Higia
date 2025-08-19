from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, StringField, SubmitField
from wtforms.validators import DataRequired


class ExamForm(FlaskForm):

    patient_identifier = StringField('Patient CPF', validators=[DataRequired()])
    patient_name = StringField('Patient Name', render_kw={'disabled': True})

    exam_type = SelectField('Exam Type', choices=[('Blood Test', 'Blood Test'), ('Audiometry', 'Audiometry')], validators=[DataRequired()])

    exam_date = DateField(validators=[DataRequired()])
    exam_hour = SelectField('Exam Hour', choices=[('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00')],
                            validators=[DataRequired()])
    submit = SubmitField('Confirm')

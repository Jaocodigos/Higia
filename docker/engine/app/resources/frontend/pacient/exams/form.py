from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, StringField, SubmitField
from wtforms.validators import DataRequired


class ExamForm(FlaskForm):

    def __init__(self, doctors, *args, **kwargs):
        doctors = [(x, x.full_name) for x in doctors] if doctors else []
        self.doctor.kwargs['choices'] = doctors
        super(ExamForm, self).__init__(*args, **kwargs)

    exam_type = SelectField('Exam Type', choices=[('blood', 'Blood Test'), ('audiometry', 'Audiometry')], validators=[DataRequired()])
    doctor = SelectField('Doctor', choices=[], validators=[DataRequired()])
    exam_date = DateField(validators=[DataRequired()])
    exam_hour = SelectField('Exam Hour', choices=[('12', '12:00'), ('13', '13:00'), ('14', '14:00')],
                            validators=[DataRequired()])
    submit = SubmitField('Confirm')

from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, StringField, SubmitField
from wtforms.validators import DataRequired


class ExamForm(FlaskForm):
    exam_date = DateField(validators=[DataRequired()])
    exam_hour = SelectField('Exam Hour', choices=[('12', '12:00'), ('13', '13:00'), ('14', '14:00')],
                            validators=[DataRequired()])

    exam_type = SelectField('Exam Type', choices=[('blood', 'Blood Test')], validators=[DataRequired()])
    submit = SubmitField('Confirm')

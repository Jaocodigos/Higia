from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField
from wtforms.validators import DataRequired

class ProfileForm(FlaskForm):

    full_name = StringField('Full Name', validators=[DataRequired()])
    identifier = StringField('CPF', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[])
    cep = StringField('Address', validators=[])
    password = PasswordField('Password')

    submit = SubmitField('Save')
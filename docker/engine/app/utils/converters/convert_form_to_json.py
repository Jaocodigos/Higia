from flask_wtf import FlaskForm
from datetime import date

def form_to_json(form: FlaskForm) -> dict:
    data  = dict()
    for f in form._fields.keys():

        if f == 'csrf_token' or f == 'submit':
            continue

        elif isinstance(form._fields[f].data, date):
            data[f] = form._fields[f].data.strftime("%d/%m/%Y")

        else:
            data[f] = form._fields[f].data

    return data

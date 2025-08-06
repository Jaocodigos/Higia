from flask_wtf import FlaskForm


def form_to_json(form: FlaskForm) -> dict:
    data  = dict()
    for f in form._fields.keys():
        if f == 'csrf_token' or f == 'submit':
            continue
        data[f] = form._fields[f].data
    return data

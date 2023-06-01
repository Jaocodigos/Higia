from marshmallow import validate, ValidationError


class UniqueNameValidator(validate.Validator):
    def __call__(self, name, model):
        if name:
            value = model.query.filter_by().first()
            if value:
                raise ValidationError("Name already exist.")
            return value
        else:
            raise ValidationError("The field 'Name' must be required.")


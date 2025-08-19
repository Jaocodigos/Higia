from flask_marshmallow import Schema
from flask_sqlalchemy.model import Model
from marshmallow import ValidationError
from flask import abort
from engine.app.config.logs import prepare_logs

log = prepare_logs(__name__)


def convert_json_to_model(model: Model, schema: Schema, data: dict, converters={}):
    try:
        schema.load(data)
    except ValidationError as ve:
        log.error(f"Error Validating data: {ve}")
        abort(400, f"Invalid data: {ve}")
    log.debug("Validated! Now creating a new model.")
    try:
        for x in data.keys():
            if x in converters.keys():
                log.debug(f"Converting {x} for pass to model")
                data[x] = converters[x](data[x])
            if hasattr(model, x):
                log.debug(f"Inserting in {x} the value {data[x]}")
                model.__setattr__(x, data[x])
    except (KeyError, ValueError) as e:
        log.error(f"Error inserting data on model: {e}")
        abort(400, "Invalid data, try again.")

    log.debug("Schema load completed! Now saving on DB.")
    try:
        model.save()
    except Exception as e:
        log.error(f"Error saving data in model '{model.__name__}': {str(e)}")
        abort(400, "An unexpected behavior occurred while saving your information, please try again.")

    return model.serialized(model.protected_fields)

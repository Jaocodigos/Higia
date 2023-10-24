import re
from engine.app.models.intern.roles import Roles


def convert_identifier(identifier):
    if len(identifier) == 14:
        if identifier[3] == '.' and identifier[7] == '.' and identifier[11] == '-':
            formatted_identifier = re.sub(r'\D', '', identifier)
            if len(formatted_identifier) == 11 and formatted_identifier.isdigit():
                return formatted_identifier
    elif len(identifier) == 11 and identifier.isdigit():
        return identifier
    return None


def convert_role_to_model(roles: list):
    model_list = list()
    for role_name in roles:
        role = Roles.query.filter_by(role_name=role_name).first()
        if role:
            model_list.append(role)
    return model_list

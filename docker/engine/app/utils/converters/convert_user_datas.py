import re


def convert_identifier(identifier):
    if len(identifier) == 14:
        if identifier[3] == '.' and identifier[7] == '.' and identifier[11] == '-':
            formatted_identifier = re.sub(r'\D', '', identifier)
            if len(formatted_identifier) == 11 and formatted_identifier.isdigit():
                return formatted_identifier
    elif len(identifier) == 11 and identifier.isdigit():
        return identifier
    return None

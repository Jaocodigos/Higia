from engine.app.config.logs import prepare_logs
import re

log = prepare_logs(__name__)


def validate_identifier(identifier, convert=False):
    if len(identifier) == 14 and identifier[3] == '.' and identifier[7] == '.' and identifier[11] == '-':
        clean_identifier = re.sub(r'\D', '', identifier)
        if len(clean_identifier) == 11 and clean_identifier.isdigit():
            if convert:
                return clean_identifier
            else:
                return identifier
        return None
    elif len(identifier) == 11 and identifier.isdigit():
        return identifier
    else:
        return None

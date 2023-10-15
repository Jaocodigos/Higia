from datetime import datetime
from engine.app.utils.converters.convert_dates import convert_string_date_to_datetime


def validate_date(string_date):
    dt = convert_string_date_to_datetime(string_date)
    if dt:
        date_now = datetime.now()
        time_left = dt - date_now
        if time_left.days < 1 and time_left.seconds < 10800:
            return False
        return True
    return False

from datetime import datetime


def convert_string_date_to_datetime(string_date):
    split_date = string_date.split('/')
    if len(split_date) == 3 and all(x.isdigit() for x in split_date):
        new_date = datetime(int(split_date[2]), int(split_date[1]), int(split_date[0]))
        return new_date
    return None

from datetime import datetime


def convert_string_date_to_datetime(string_date):
    split_date = string_date.split('/')
    if len(split_date) == 3 and all(x.isdigit() for x in split_date):
        new_date = datetime(int(split_date[2]), int(split_date[1]), int(split_date[0]))
        return new_date
    if len(split_date) == 3 and ',' in split_date[2]:
        year_and_hour = split_date[2].split(',')
        split_time = year_and_hour[1].split(':')
        new_date = datetime(int(year_and_hour[0]), int(split_date[1]), int(split_date[0]), int(split_time[0]), int(split_time[1]))
        return new_date
    return None

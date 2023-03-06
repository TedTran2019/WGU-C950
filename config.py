from datetime import datetime, time, timedelta

CURRENT_TIME = time(hour=8)


def parse_time(time_string):
    return datetime.strptime(time_string, '%I:%M %p').time()


def increment_time(time, minutes_added):
    delta = timedelta(minutes=minutes_added)
    return (datetime.combine(datetime.min, time) + delta).time()


def increment_global_time(minutes):
    global CURRENT_TIME
    CURRENT_TIME = increment_time(CURRENT_TIME, minutes)

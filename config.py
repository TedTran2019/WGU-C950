CURRENT_TIME = "08:00"


def parse_time(time_string):
    hours, minutes = time_string.split(':')
    meridiem = minutes[3:]
    minutes = minutes[:2]
    if len(hours) == 1:
        hours = '0' + hours
    if meridiem == 'PM':
        hours = int(hours) + 12
    return str(hours) + ':' + minutes


def increment_time(time_string, minutes_added):
    hours, minutes = time_string.split(':')
    minutes = int(minutes) + minutes_added
    hours = int(hours)
    while minutes >= 60:
        minutes -= 60
        hours += 1
    while hours >= 24:
        hours -= 24
    if hours < 10:
        hours = '0' + str(hours)
    if minutes < 10:
        minutes = '0' + str(minutes)
    return str(hours) + ':' + str(minutes)


def increment_global_time(minutes):
    global CURRENT_TIME
    CURRENT_TIME = increment_time(CURRENT_TIME, minutes)

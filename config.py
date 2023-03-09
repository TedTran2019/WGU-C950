# Every method here is O(1) time complexity and O(1) space complexity
from datetime import datetime, time, timedelta

CURRENT_TIME = time(hour=8)


# Parses a string in the format of 'HH:MM AM/PM' into a time object
def parse_time(time_string):
    return datetime.strptime(time_string, '%I:%M %p').time()


# Adds minutes to a time object and returns the new time object
def increment_time(time, minutes_added):
    delta = timedelta(minutes=minutes_added)
    return (datetime.combine(datetime.min, time) + delta).time()


# Increments global time by minutes
def increment_global_time(minutes):
    global CURRENT_TIME
    CURRENT_TIME = increment_time(CURRENT_TIME, minutes)


# Sets global time to time
def set_global_time(time):
    global CURRENT_TIME
    CURRENT_TIME = time


# Returns the difference between two time objects
def subtract_times(time1, time2):
    return (datetime.combine(datetime.min, time1) - datetime.combine(datetime.min, time2))

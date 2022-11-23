"""Useful utils for the project."""

import calendar
from datetime import datetime


def time_to_string(time_data):
    """Cast time to string HH:MM."""
    return time_data.strftime("%H:%M")


def string_to_time(string):
    """Cast string HH:MM to time."""
    return datetime.strptime(string, "%H:%M").time()


def generate_working_time(start_time: str = "", end_time: str = ""):
    """Generates working time."""
    week_days = [day for day in calendar.HTMLCalendar.cssclasses]
    working_time = {day: [start_time, end_time] for day in week_days}
    if not start_time and not end_time:
        working_time = dict.fromkeys(week_days, [])
    return working_time


def string_interval_to_time_interval(str_interval: list):
    """Returns list of time objects."""
    return list(map(string_to_time, str_interval))

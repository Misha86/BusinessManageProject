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
    working_time = {day.capitalize(): [start_time, end_time] for day in week_days}
    if not start_time and not end_time:
        working_time = dict.fromkeys(week_days, [])
    return working_time


def generate_working_time_intervals(start_time: str = "", end_time: str = ""):
    """Generates working time intervals."""
    working_time = generate_working_time(start_time, end_time)
    working_time_intervals = {k: [v] for k, v in working_time.items()}
    return working_time_intervals


def string_interval_to_time_interval(str_interval: list):
    """Returns list of time objects."""
    return list(map(string_to_time, str_interval))


def time_interval_to_string_interval(str_interval: list):
    """Returns list of string objects."""
    return list(map(time_to_string, str_interval))


def is_inside_interval(main_interval: tuple, inner_interval: tuple):
    """Return True if inner interval is inside main_interval."""
    return (
        inner_interval[0] >= main_interval[0]
    ) and (
        inner_interval[1] <= main_interval[1]
    )

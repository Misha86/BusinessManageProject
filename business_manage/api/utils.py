"""Useful utils for the project."""

import calendar
from datetime import datetime, time

from django.contrib.auth import get_user_model
from django.db.models import CharField, Value
from django.db.models.functions import Concat


def time_to_string(time_data):
    """Cast time to string HH:MM."""
    return time_data.strftime("%H:%M")


def string_to_time(string):
    """Cast string HH:MM to time."""
    return datetime.strptime(string, "%H:%M").time()


def generate_working_time(start_time: str = "", end_time: str = "") -> dict[str, list[str]]:
    """Generates working time."""
    week_days = [day.capitalize() for day in calendar.HTMLCalendar.cssclasses]
    working_time = {day: [start_time, end_time] for day in week_days}
    if not start_time and not end_time:
        working_time = dict.fromkeys(week_days, [])
    return working_time


def generate_working_time_intervals(start_time: str = "", end_time: str = "") -> dict[str, list[list[str]]]:
    """Generates working time intervals."""
    working_time = generate_working_time(start_time, end_time)
    return {k: [v] for k, v in working_time.items()}


def string_interval_to_time_interval(str_interval: list[str]) -> list[time]:
    """Returns list of time objects."""
    return list(map(string_to_time, str_interval))


def time_interval_to_string_interval(str_interval: list[time]) -> list[str]:
    """Returns list of string objects."""
    return list(map(time_to_string, str_interval))


def is_inside_interval(main_interval: list[time], inner_interval: list[time]) -> bool:
    """Return True if inner interval is inside main_interval."""
    return (inner_interval[0] >= main_interval[0]) and (inner_interval[1] <= main_interval[1])


def get_location_choices(model_class):
    """Get locations' data for choice field."""
    try:
        return list(model_class.objects.filter(working_time__isnull=False).order_by("name").values_list("id", "name"))
    except Exception:
        return []


def get_specialist_choices():
    """Get specialists' data for choice field."""
    try:
        user_model = get_user_model()
        return list(
            user_model.specialists.filter(schedule__isnull=False)
            .order_by("first_name", "last_name")
            .annotate(full_name=Concat("last_name", Value(" ["), "email", Value("]"), output_field=CharField()))
            .values_list("id", "full_name")
        )
    except Exception:
        return []

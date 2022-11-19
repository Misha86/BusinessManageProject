"""Useful utils for the project."""

import calendar
from datetime import timedelta, datetime, time
from rest_framework.exceptions import ValidationError


def time_to_string(time_data):
    """Cast time to string HH:MM."""
    return time_data.strftime("%H:%M")


def string_to_time(string):
    """Cast string HH:MM to time."""
    return datetime.strptime(string, "%H:%M").time()


def validate_rounded_minutes_seconds(time_value):
    """Validate time value.

    Time must have zero seconds and minutes multiples of 5
    """
    assert isinstance(time_value, (datetime, time, timedelta)), \
        "Only datetime, time or timedelta objects"

    if isinstance(time_value, (datetime, time)):
        if isinstance(time_value, datetime):
            time_value = time_value.time()

        if time_value.minute % 5 and time_value.second != 0:
            raise ValidationError(
                {time_value: "Time value must have zero seconds and minutes multiples of 5"}
            )

    if isinstance(time_value, timedelta):
        if (time_value.seconds / 60) % 5:
            raise ValidationError(
                {time_value: "Time value must have zero seconds and minutes multiples of 5"}
            )


def validate_match_format(field_name, values_list):
    """Validate format for list with time range."""
    time_data = []
    for value in values_list:
        try:
            time_data.append(string_to_time(value))
        except ValueError as ex_massage:
            raise ValidationError({field_name: ex_massage})
    return time_data


def validate_start_end_time(field_name, list_time_data):
    """Validate start time and end time."""
    if list_time_data:
        try:
            start_time, end_time = list_time_data
        except ValueError:
            raise ValidationError(
                {field_name: "Time range should be contain "
                             "start and end time together or empty range"}
            )

        if start_time > end_time:
            raise ValidationError(
                {field_name: "Start time should be more than end time"}
            )


def validate_working_time(json):
    """Validate json for working time for every day."""
    for key, value in json.items():
        list_time_data = validate_match_format(key, value)
        validate_start_end_time(key, list_time_data)
        map(validate_rounded_minutes_seconds, list_time_data)


def generate_working_time(start_time: str = "", end_time: str = ""):
    """Generates working time."""
    week_days = [day.capitalize()
                 for day in calendar.HTMLCalendar.cssclasses]
    return {day: [start_time, end_time] for day in week_days}

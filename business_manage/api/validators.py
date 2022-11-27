"""Validators for business_manage project."""

import calendar
import itertools

from django.utils import timezone
from datetime import time
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .utils import string_interval_to_time_interval, string_to_time


def validate_rounded_minutes(time_value):
    """Validate time value.

    Time must have zero seconds and minutes multiples of 5
    """
    if isinstance(time_value, (timezone.datetime, time)):
        if isinstance(time_value, timezone.datetime):
            time_value = time_value.time()

        if time_value.minute % 5 or time_value.second != 0:
            raise ValidationError(
                {time_value.strftime("%H:%M:%S"): "Time value must have zero "
                                                  "seconds and minutes multiples of 5."}
            )


def validate_rounded_minutes_seconds(delta_time_value):
    """Validate timedelta value.

    Time must have zero seconds and minutes multiples of 5
    """
    if isinstance(delta_time_value, timezone.timedelta):
        if (delta_time_value.seconds / 60) % 5:
            raise ValidationError(
                {
                    f"{delta_time_value}":
                        "Duration value must have zero seconds and minutes multiples of 5."
                }
            )


def validate_match_time_format(field_name: str, str_interval: list[str]):
    """Validate format for value from time interval."""
    try:
        string_interval_to_time_interval(str_interval)
    except ValueError as ex_massage:
        raise ValidationError({field_name: ex_massage})


def validate_start_end_time(field_name, time_interval: list[time]):
    """Validate start time and end time."""
    if time_interval:
        try:
            start_time, end_time = time_interval
        except ValueError:
            raise ValidationError(
                {
                    field_name: "Time range should be contain "
                                "start and end time together or empty range."
                }
            )
        if start_time >= end_time:
            raise ValidationError(
                {field_name: "Start time should be more than end time."}
            )


def validate_working_time_interval(week_day: str, str_interval: list[str]):
    """Validate single time interval (["10:30", "11:40"])."""
    validate_match_time_format(week_day, str_interval)

    time_interval = string_interval_to_time_interval(str_interval)

    validate_start_end_time(week_day, time_interval)

    [validate_rounded_minutes(time_data) for time_data in time_interval]


def validate_working_time(json: dict):
    """Validate json for working time for every day."""
    for day, intervals in json.items():
        validate_working_time_interval(day, intervals)


def validate_working_time_intervals(json: dict):
    """Validate time ranges for working time for every day.

    Specialist can have more than one time range during working day.
    """
    for day, intervals in json.items():
        for interval in intervals:
            validate_working_time_interval(day, interval)


def validate_working_time_values(json: dict):
    """Validate time intervals values for working time for every day.

    Time intervals should not be covering each other.
    """
    for day, intervals in json.items():
        time_intervals = map(lambda x:
                             [
                                 string_to_time(x[0]),
                                 string_to_time(x[1])
                             ],
                             intervals)
        sorted_intervals = sorted(time_intervals, key=lambda x: x[0])
        intervals_values = list(itertools.chain(*sorted_intervals))
        sorted_intervals_values = sorted(intervals_values)

        if intervals_values != sorted_intervals_values:
            raise ValidationError(
                {day: "Time ranges cannot cover each other."}
            )


def validate_specialist(user_data):
    """Validate user is specialist."""
    try:
        user_model = get_user_model()
        user = user_model.objects.get(id=user_data)
    except TypeError:
        user = user_data
    if not user.is_specialist:
        full_name = user.get_full_name()
        raise ValidationError(
            {full_name: f"{full_name} should be specialist."})


def validate_datetime_is_future(value):
    """Datetime values should have future date."""
    if timezone.now() > value:
        raise ValidationError(
            {
                value.strftime("%H:%M:%S"):
                    f"DateTime value {value} should have future datetime."
            }
        )


def validate_days_name(value):
    """Check days name are correct."""
    week_days = list(map(str.capitalize, calendar.HTMLCalendar.cssclasses))
    for name in value.keys():
        if name not in week_days:
            raise ValidationError(
                {
                    f"{name}":
                        f"Day name should be one of these {week_days}."
                }
            )

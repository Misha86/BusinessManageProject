"""Validators for business_manage project."""

import calendar
import itertools
from datetime import time, timedelta
from operator import itemgetter

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .utils import string_interval_to_time_interval, string_to_time


def validate_rounded_minutes_base(time_value: time) -> str | None:
    """Base function for validate time value.

    Time must have zero seconds and minutes multiples of 5
    """
    if isinstance(time_value, (timezone.datetime, time)):
        if isinstance(time_value, timezone.datetime):
            time_value = time_value.time()

        if time_value.minute % 5 or time_value.second != 0:
            return "Time value must have zero seconds and minutes multiples of 5."


def validate_rounded_minutes_working_time(time_value: time, week_day: str) -> None:
    """Validate time value.

    Time must have zero seconds and minutes multiples of 5
    """
    if error_message := validate_rounded_minutes_base(time_value):
        raise ValidationError({week_day: error_message})


def validate_rounded_minutes(time_value: time) -> None:
    """Validate time value.

    Time must have zero seconds and minutes multiples of 5
    """
    if error_message := validate_rounded_minutes_base(time_value):
        raise ValidationError(error_message)


def validate_rounded_minutes_seconds(delta_time_value: timedelta) -> None:
    """Validate timedelta value.

    Time must have zero seconds and minutes multiples of 5
    """
    if isinstance(delta_time_value, timezone.timedelta) and (delta_time_value.seconds / 60) % 5:
        raise ValidationError("Duration value must have zero seconds and minutes multiples of 5.")


def validate_match_time_format(field_name: str, str_interval: list[str]) -> None:
    """Validate format for value from time interval."""
    try:
        string_interval_to_time_interval(str_interval)
    except ValueError as ex_massage:
        raise ValidationError({field_name: ex_massage}) from ex_massage


def validate_start_end_time(field_name: str, time_interval: list[time]) -> None:
    """Validate start time and end time."""
    if time_interval:
        try:
            start_time, end_time = time_interval
        except ValueError as ex:
            raise ValidationError(
                {field_name: "Time range should be contain start and end time together or empty range."}
            ) from ex

        if start_time >= end_time:
            raise ValidationError({field_name: "Start time should be more than end time."})


def validate_working_time_interval(week_day: str, str_interval: list[str]) -> None:
    """Validate single time interval (["10:30", "11:40"])."""
    validate_match_time_format(week_day, str_interval)

    time_interval = string_interval_to_time_interval(str_interval)

    validate_start_end_time(week_day, time_interval)

    for time_data in time_interval:
        validate_rounded_minutes_working_time(time_data, week_day)


def validate_working_time(json: dict[str, list[str]]) -> None:
    """Validate json for working time for every day."""
    for day, intervals in json.items():
        validate_working_time_interval(day, intervals)


def validate_working_time_intervals(json: dict[str, list[list[str]]]) -> None:
    """Validate time ranges for working time for every day.

    Specialist can have more than one time range during working day.
    """
    for day, intervals in json.items():
        for interval in intervals:
            validate_working_time_interval(day, interval)


def validate_working_time_values(json: dict[str, list[str]]) -> None:
    """Validate time intervals values for working time for every day.

    Time intervals should not be covering each other.
    """
    for day, intervals in json.items():
        time_intervals = map(lambda x: [string_to_time(x[0]), string_to_time(x[1])], intervals)
        sorted_intervals = sorted(time_intervals, key=itemgetter(0))
        intervals_values = list(itertools.chain(*sorted_intervals))
        sorted_intervals_values = sorted(intervals_values)

        if intervals_values != sorted_intervals_values:
            raise ValidationError({day: "Time ranges cannot cover each other."})


def validate_specialist(user_data):
    """Validate user is specialist."""
    try:
        user_model = get_user_model()
        user = user_model.objects.get(id=user_data)
    except TypeError:
        user = user_data
    if not user.is_specialist:
        full_name = user.get_full_name()
        raise ValidationError({"specialist": f"{full_name} should be specialist."})


def validate_datetime_is_future(value):
    """Datetime values should have future date."""
    if timezone.now() > value:
        raise ValidationError("DateTime value should have future datetime.")


def validate_days_name(value):
    """Check days name are correct."""
    week_days = list(map(str.capitalize, calendar.HTMLCalendar.cssclasses))
    for name in value.keys():
        if name not in week_days:
            raise ValidationError(f"Day name should be one of these {week_days}.")

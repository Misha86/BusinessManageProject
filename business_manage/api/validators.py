"""Validators for business_manage project."""

from django.utils import timezone
from datetime import time
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .utils import string_to_time


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


def validate_match_time_format(field_name, values_list):
    """Validate format for value from time range."""
    time_data = []
    for value in values_list:
        try:
            time_data.append(string_to_time(value))
        except ValueError as ex_massage:
            if ex_massage.__str__().count("unconverted data remains."):
                raise ValidationError(
                    {field_name: "Time value must have zero seconds and minutes multiples of 5."}
                )
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
                             "start and end time together or empty range."}
            )
        if start_time >= end_time:
            raise ValidationError(
                {field_name: "Start time should be more than end time."}
            )


def validate_working_time(json):
    """Validate json for working time for every day."""
    for key, value in json.items():
        list_time_data = validate_match_time_format(key, value)
        validate_start_end_time(key, list_time_data)
        [validate_rounded_minutes(time_data) for time_data in list_time_data]


def validate_specialist(user_data):
    """Validate user is specialist."""
    try:
        user_model = get_user_model()
        user = user_model.objects.get(id=user_data)
    except TypeError:
        user = user_data
    if not user.groups.filter(name="Specialist"):
        full_name = user.get_full_name().title()
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

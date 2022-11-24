"""Services for Appointment model."""

from django.db.models import Q
from rest_framework.exceptions import ValidationError

from api.models import Appointment, CustomUser, Location
from api.utils import is_inside_interval, string_interval_to_time_interval


def is_appointment_fit_datetime(a_interval: tuple,
                                specialist: CustomUser,
                                location: Location) -> bool:
    """Check an appointment datetime interval.

    Return True if the time slot is empty for creating an appointment else False.
    """
    appointments = Appointment.objects.filter(
        Q(start_time__range=a_interval)
        | Q(end_time__range=a_interval),
        location=location, specialist=specialist
    )
    return appointments.exists()


def is_appointment_fit_specialist_time(a_interval: tuple, specialist: CustomUser) -> bool:
    """Check an appointment time interval.

    Return True if appointment time interval is inside
    one of specialist schedule working time intervals.
    """
    start_time, end_time = a_interval
    working_time = specialist.schedule.working_time
    week_day = start_time.strftime("%a")
    string_intervals = working_time.get(week_day)

    if not string_intervals:
        return True

    specialists_intervals = list(
        map(string_interval_to_time_interval, string_intervals)
    )

    appointment_interval = (start_time.time(), end_time.time())

    return any(map(lambda x: is_inside_interval(x, appointment_interval),
                   specialists_intervals))


def is_appointment_fit_location_time(a_interval: tuple, location: Location) -> bool:
    """Check an appointment time interval.

    Return True if appointment time interval is inside
    location working time interval.
    """
    start_time, end_time = a_interval
    working_time = location.working_time
    week_day = start_time.strftime("%a")
    string_interval = working_time.get(week_day)

    if not string_interval:
        return True

    location_interval = string_interval_to_time_interval(string_interval)

    appointment_interval = (start_time.time(), end_time.time())

    return is_inside_interval(location_interval, appointment_interval)


def validate_free_time_interval(a_interval: tuple, specialist: CustomUser, location: Location):
    """Check time interval for creating new appointment."""
    if is_appointment_fit_datetime(a_interval, specialist, location):
        raise ValidationError(
            {"datetime interval": "Appointments have already created for this datetime interval."}
        )

    if is_appointment_fit_specialist_time(a_interval, specialist):
        specialist_name = specialist.get_full_name()
        raise ValidationError(
            {"time interval": f"{specialist_name} doesn't work at this time interval."}
        )

    if is_appointment_fit_location_time(a_interval, location):
        raise ValidationError(
            {"time interval": f"{location.name} doesn't work at this time interval."}
        )

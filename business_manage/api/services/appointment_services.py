"""Services for Appointment model."""

from datetime import datetime

from django.db.models import Q
from django.utils.timezone import localtime
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from api.models import Appointment, CustomUser, Location, SpecialistSchedule
from api.services.schedule_services import get_working_day
from api.utils import (
    is_inside_interval,
    string_interval_to_time_interval,
    time_interval_to_string_interval,
)


def is_appointment_fit_datetime(a_interval: list[datetime], specialist: CustomUser, location: Location) -> bool:
    """Check an appointment datetime interval.

    Return True if the time slot is empty for creating an appointment else False.
    """
    appointments = Appointment.objects.filter(
        Q(start_time__range=a_interval) | Q(end_time__range=a_interval),
        location=location,
        specialist=specialist,
    )
    return not appointments.exists()


def is_specialist_schedule(specialist):
    """Check the specialist has schedule."""
    return hasattr(specialist, "schedule")


def is_appointment_fit_specialist_time(a_interval: list[datetime], specialist: CustomUser) -> bool:
    """Check an appointment time interval.

    Return True if appointment time interval is inside
    one of specialist schedule working time intervals.
    """
    start_time, end_time = a_interval
    schedule = get_object_or_404(SpecialistSchedule, specialist=specialist)
    string_intervals = get_working_day(schedule.working_time, start_time)

    if not string_intervals:
        return True

    specialists_intervals = list(map(string_interval_to_time_interval, string_intervals))

    appointment_interval = [localtime(start_time).time(), localtime(end_time).time()]

    return any(map(lambda x: is_inside_interval(x, appointment_interval), specialists_intervals))


def is_appointment_fit_location_time(a_interval: list[datetime], location: Location) -> bool:
    """Check an appointment time interval.

    Return True if appointment time interval is inside
    location working time interval.
    """
    start_time, end_time = a_interval
    string_interval = get_working_day(location.working_time, start_time)

    if not string_interval:
        return True

    location_interval = string_interval_to_time_interval(string_interval)

    appointment_interval = [start_time.time(), end_time.time()]

    return is_inside_interval(location_interval, appointment_interval)


def validate_free_time_interval(a_interval: list[datetime], specialist: CustomUser, location: Location) -> None:
    """Check time interval for creating new appointment."""
    if not is_appointment_fit_datetime(a_interval, specialist, location):
        raise ValidationError({"detail": "Appointments have already created for this datetime."})

    specialist_name = specialist.get_full_name()
    if not is_specialist_schedule(specialist):
        raise ValidationError({"specialist": f"{specialist_name} hasn't had schedule jet."})

    if not is_appointment_fit_specialist_time(a_interval, specialist):
        raise ValidationError({"specialist": f"{specialist_name} doesn't work at this time interval."})

    if not is_appointment_fit_location_time(a_interval, location):
        raise ValidationError({"location": f"{location.name} doesn't work at this time interval."})


def get_appointments_time_intervals(specialist: CustomUser, date: datetime) -> list[list[str]]:
    """Get all appointments working intervals for a specific specialist and concrete date."""
    appointments = Appointment.objects.filter(specialist=specialist, start_time__date=date)

    return [
        time_interval_to_string_interval(
            [localtime(appointment.start_time).time(), localtime(appointment.end_time).time()]
        )
        for appointment in appointments
    ]

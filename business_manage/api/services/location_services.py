"""Services for Location model."""

from api.models import Location
import calendar


def get_locations_with_working_days():
    """Get all locations which have at least one working day."""
    default_dict = dict.fromkeys([day for day in calendar.HTMLCalendar.cssclasses], [])
    return Location.objects.exclude(working_time=default_dict)

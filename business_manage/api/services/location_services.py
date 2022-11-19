"""Services for Location model."""

from api.models import Location
from api.utils import generate_working_time


def get_locations_with_working_days():
    """Get all locations which have at least one working day."""
    default_dict = generate_working_time()
    return Location.objects.exclude(working_time=default_dict)

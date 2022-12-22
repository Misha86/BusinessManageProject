"""Module for custom django_filters."""

from datetime import datetime

from django.db.models import Q
from django_filters import rest_framework as filters

from .models import CustomUser


class SpecialistFilter(filters.FilterSet):
    """Class to filter specialists."""

    date = filters.CharFilter(method="working_day_filter", field_name="schedule")

    class Meta:
        model = CustomUser
        fields = ["position"]

    def working_day_filter(self, queryset, name, value):
        """Filter specialists who works in the some date."""
        try:
            week_day = datetime.strptime(value, "%Y-%m-%d").strftime("%a")
            return queryset.exclude(Q(schedule__isnull=True) | Q(**{f"schedule__working_time__{week_day}": []}))
        except ValueError:
            return queryset.none()

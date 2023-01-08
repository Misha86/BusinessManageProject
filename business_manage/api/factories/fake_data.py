"""Module for get custom fake data."""

from datetime import timedelta
import factory.fuzzy
from django.utils import timezone


def get_future_datetime(start=1, end=10, force_hour=13, force_minute=30):
    return factory.fuzzy.FuzzyDateTime(
        timezone.localtime(timezone.now()) + timedelta(days=start),
        timezone.localtime(timezone.now()) + timedelta(days=end),
        force_hour=force_hour,
        force_minute=force_minute,
        force_second=0,
        force_microsecond=0,
    )
"""Services for Schedule model."""

import datetime
import itertools

from api.models import CustomUser
from api.utils import is_inside_interval, string_interval_to_time_interval


def get_working_day(specialist: CustomUser, date: datetime):
    """Get specialist working day using datetime argument."""
    week_day = date.strftime("%a")
    working_intervals = specialist.schedule.working_time.get(week_day)
    return working_intervals


def get_free_time_intervals(schedule_intervals: list, appointments_intervals: list):
    """Get all free intervals for a specific specialist."""
    schedule_intervals = [string_interval_to_time_interval(i) for i in schedule_intervals]

    appointments_intervals.extend(schedule_intervals)

    a_intervals_values = sorted(itertools.chain(*appointments_intervals))

    def filter_intervals(item):
        inside_intervals = any(is_inside_interval(s, item) for s in schedule_intervals)
        return len(set(item)) != 1 and inside_intervals

    free_intervals = zip(a_intervals_values[::2], a_intervals_values[1::2])
    free_working_intervals = list(filter(filter_intervals, free_intervals))

    return free_working_intervals

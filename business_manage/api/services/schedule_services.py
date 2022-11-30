"""Services for Schedule model."""

from datetime import datetime
import itertools

from api.utils import is_inside_interval, string_interval_to_time_interval, time_interval_to_string_interval


def get_working_day(working_time: dict[str, list[str]], date_value: datetime) -> list[str]:
    """Get specialist working day using datetime argument."""
    week_day = date_value.strftime("%a")
    return working_time.get(week_day, [])


def get_free_time_intervals(
    schedule_intervals: list[list[str]], appointments_intervals: list[list[str]]
) -> list[list[str]]:
    """Get all free intervals for a specific specialist."""
    schedule_time_intervals = [string_interval_to_time_interval(s_i) for s_i in schedule_intervals]
    appointments_time_intervals = [string_interval_to_time_interval(a_i) for a_i in appointments_intervals]

    a_intervals_values = sorted(
        itertools.chain(
            *appointments_time_intervals,
            *schedule_time_intervals,
        )
    )

    def filter_intervals(item):
        inside_intervals = any(is_inside_interval(s, item) for s in schedule_time_intervals)
        return len(set(item)) != 1 and inside_intervals

    free_intervals = zip(a_intervals_values[::2], a_intervals_values[1::2])
    free_working_intervals = filter(filter_intervals, free_intervals)

    return list(map(time_interval_to_string_interval, free_working_intervals))

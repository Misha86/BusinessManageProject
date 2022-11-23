"""The module includes serializers for working time in a week."""

from rest_framework import serializers


class WorkingTimeSerializer(serializers.Serializer):
    """WorkingTime serializer for working hours.

    Provides proper business creation and validation based on set working hours.
    """

    Mon = serializers.ListField(max_length=3, default=[])
    Tue = serializers.ListField(max_length=3, default=[])
    Wed = serializers.ListField(max_length=3, default=[])
    Thu = serializers.ListField(max_length=3, default=[])
    Fri = serializers.ListField(max_length=3, default=[])
    Sat = serializers.ListField(max_length=3, default=[])
    Sun = serializers.ListField(max_length=3, default=[])

    # def to_representation(self, instance):
    #     """Remove week days without schedule."""
    #     return {k: v for k, v in instance.items() if v}

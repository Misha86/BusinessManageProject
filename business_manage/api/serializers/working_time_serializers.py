"""The module includes serializers for working time in a week."""

from rest_framework import serializers


class WorkingTimeSerializer(serializers.Serializer):
    """WorkingTime serializer for working hours.

    Provides proper business creation and validation based on set working hours.
    """

    mon = serializers.ListField(max_length=2, default=[])
    tue = serializers.ListField(max_length=2, default=[])
    wed = serializers.ListField(max_length=2, default=[])
    thu = serializers.ListField(max_length=2, default=[])
    fri = serializers.ListField(max_length=2, default=[])
    sat = serializers.ListField(max_length=2, default=[])
    sun = serializers.ListField(max_length=2, default=[])

    # def to_representation(self, instance):
    #     """Remove week days without schedule."""
    #     return {k: v for k, v in instance.items() if v}

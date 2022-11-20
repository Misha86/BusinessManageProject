"""The module includes serializers for Location model."""

from rest_framework import serializers
from api.models import Location
from api.validators import validate_working_time


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

    def to_representation(self, instance):
        """Remove week days without schedule."""
        return {k: v for k, v in instance.items() if v}


class LocationSerializer(serializers.ModelSerializer):
    """Serializer to receive and create a specific location."""

    working_time = WorkingTimeSerializer(validators=[validate_working_time])

    class Meta:
        """Class with a model and model fields for serialization."""

        model = Location
        fields = "__all__"

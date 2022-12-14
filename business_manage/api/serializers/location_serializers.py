"""The module includes serializers for Location model."""

from rest_framework import serializers
from api.models import Location
from api.serializers.working_time_serializers import WorkingTimeSerializer
from api.validators import validate_working_time


class LocationSerializer(serializers.ModelSerializer):
    """Serializer to receive and create a specific location."""

    working_time = WorkingTimeSerializer(validators=[validate_working_time])

    class Meta:
        """Class with a model and model fields for serialization."""

        model = Location
        fields = ["name", "address", "working_time"]

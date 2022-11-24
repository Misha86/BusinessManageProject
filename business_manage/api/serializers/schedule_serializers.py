"""The module includes serializers for Location model."""

from rest_framework import serializers
from api.models import SpecialistSchedule
from api.serializers.working_time_serializers import WorkingTimeSerializer
from api.validators import validate_working_time_intervals, validate_working_time_values


class SpecialistScheduleDetailSerializer(serializers.ModelSerializer):
    """Serializer to retrieve, update or delete schedule for specific specialist."""

    working_time = WorkingTimeSerializer(validators=[validate_working_time_intervals,
                                                     validate_working_time_values])

    class Meta:
        """Class with a model and model fields for serialization."""

        model = SpecialistSchedule
        fields = ["working_time"]


class SpecialistScheduleSerializer(SpecialistScheduleDetailSerializer):
    """Serializer to receive and create schedules for specialists."""

    class Meta(SpecialistScheduleDetailSerializer.Meta):
        """Class with a model and model fields for serialization."""
        fields = SpecialistScheduleDetailSerializer.Meta.fields + ["specialist"]

    def to_representation(self, instance):
        """Change displaying schedule specialist from id to full name."""
        full_name = instance.specialist.get_full_name()
        data = super().to_representation(instance)
        data["specialist"] = full_name
        return data

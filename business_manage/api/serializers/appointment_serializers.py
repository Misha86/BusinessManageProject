"""The module includes serializers for Appointment model."""

from rest_framework import serializers
from api.models import Appointment
from api.validators import validate_start_end_time


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer to receive and create a specific appointments."""

    is_active = serializers.BooleanField(initial=True, default=True)

    class Meta:
        """Class with a model and model fields for serialization."""

        model = Appointment
        exclude = ["id", "created_at", "update_at"]
        read_only_fields = ["end_time"]

    def validate(self, data):
        """Validate data before saving."""
        start_time = data.get("start_time")
        duration = data.get("duration")
        end_time = start_time + duration
        validate_start_end_time("time range", [start_time, end_time])
        return data

    def to_representation(self, instance):
        """Change displaying specialist id to full name."""
        specialist = instance.specialist
        location = instance.location
        appointment = super().to_representation(instance)
        appointment["specialist"] = specialist.get_full_name()
        appointment["location"] = location.name
        return appointment

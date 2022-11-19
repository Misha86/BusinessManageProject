"""The module includes serializers for Appointment model."""

from rest_framework import serializers
from api.models import Appointment
from api.utils import validate_start_end_time


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer to receive and create a specific appointments."""

    is_active = serializers.BooleanField(initial=True)

    class Meta:
        """Class with a model and model fields for serialization."""

        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        """Validate fields before save."""
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        validate_start_end_time("time range", [start_time, end_time])
        return attrs

    def to_representation(self, instance):
        """Change displaying specialist id to full name."""
        specialist = instance.specialist
        appointment = super().to_representation(instance)
        appointment["specialist"] = specialist.get_full_name()
        return appointment

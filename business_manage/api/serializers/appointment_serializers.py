"""The module includes serializers for Appointment model."""

from rest_framework import serializers
from api.models import Appointment
from api.services.appointment_services import validate_free_time_interval
from api.validators import validate_start_end_time
from api.models import CustomUser, Location
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer to receive and create a specific appointments."""

    is_active = serializers.BooleanField(initial=True, default=True)
    specialist = serializers.ChoiceField(
        # choices=CustomUser.specialists.filter(schedule__isnull=False)
        choices=CustomUser.specialists.all()
        .order_by("first_name", "last_name")
        .annotate(full_name=Concat("last_name", Value(" ["), "email", Value("]"), output_field=CharField()))
        .values_list("id", "full_name"),
        help_text="This field is required",
    )

    location = serializers.ChoiceField(
        choices=Location.objects.filter(working_time__isnull=False).order_by("name").values_list("id", "name"),
        help_text="This field is required",
    )

    class Meta:
        """Class with a model and model fields for serialization."""

        model = Appointment
        exclude = ["id", "created_at", "update_at"]
        read_only_fields = ["end_time"]

    def validate(self, attrs):
        """Validate data before saving."""
        start_time = attrs.get("start_time")
        specialist = get_object_or_404(CustomUser, id=attrs.get("specialist"))
        location = get_object_or_404(Location, id=attrs.get("location"))
        duration = attrs.get("duration")
        end_time = start_time + duration
        validate_start_end_time("time range", [start_time, end_time])
        validate_free_time_interval([start_time, end_time], specialist, location)
        attrs.update(dict(specialist=specialist, location=location))
        return attrs

    def to_representation(self, instance):
        """Change displaying specialist id to the full name and location id to the name."""
        specialist = instance.specialist
        location = instance.location
        appointment = super().to_representation(instance)
        appointment["specialist"] = specialist.get_full_name()
        appointment["location"] = location.name
        return appointment

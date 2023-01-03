"""The module includes serializers for Location model."""

from api.models import SpecialistSchedule
from api.serializers.working_time_serializers import WorkingTimeSerializer
from api.validators import validate_working_time_intervals, validate_working_time_values
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from rest_framework import serializers

from ..models import CustomUser


class SpecialistScheduleDetailSerializer(serializers.ModelSerializer):
    """Serializer to retrieve, update or delete schedule for specific specialist."""

    working_time = WorkingTimeSerializer(validators=[validate_working_time_intervals, validate_working_time_values])

    class Meta:
        """Class with a model and model fields for serialization."""

        model = SpecialistSchedule
        fields = ["working_time"]


class SpecialistScheduleSerializer(SpecialistScheduleDetailSerializer):
    """Serializer to receive and create schedules for specialists."""

    default_error_messages = {
        "specialist_exist": "Specialist with '{id}' doesn't exist.",
        "specialist_schedule": "Schedule with this specialist already exists.",
    }

    # specialist = serializers.EmailField(required=True)
    specialist = serializers.ChoiceField(
        choices=CustomUser.specialists.filter(schedule=None)
        .order_by("first_name", "last_name")
        .annotate(full_name=Concat("last_name", Value(" ["), "email", Value("]"), output_field=CharField()))
        .values_list("id", "full_name"),
        help_text="This field is required",
    )

    class Meta(SpecialistScheduleDetailSerializer.Meta):
        """Class with a model and model fields for serialization."""

        fields = ["specialist"] + SpecialistScheduleDetailSerializer.Meta.fields

    def to_representation(self, instance):
        """Change displaying schedule specialist from id to full name."""
        full_name = instance.specialist.get_full_name()
        data = super().to_representation(instance)
        data["specialist"] = full_name
        return data

    def validate_specialist(self, id):
        """Check specialist existing, specialist schedule existing and return specialist instance."""
        try:
            specialist = CustomUser.specialists.get(id=id)
        except ObjectDoesNotExist:
            self.fail("specialist_exist", id=id)

        schedule = SpecialistSchedule.objects.filter(specialist=specialist)

        if schedule.exists():
            self.fail("specialist_schedule")

        return specialist

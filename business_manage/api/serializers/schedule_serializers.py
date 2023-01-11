"""The module includes serializers for Location model."""

from api.models import SpecialistSchedule
from api.serializers.working_time_serializers import WorkingTimeSerializer
from api.validators import validate_working_time_intervals, validate_working_time_values
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from ..models import CustomUser
from ..utils import get_specialist_choices


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

    specialist = serializers.ChoiceField(choices=get_specialist_choices(), help_text="This field is required")

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

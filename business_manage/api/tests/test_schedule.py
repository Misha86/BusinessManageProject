"""The module includes tests for Schedule model, serializers and views."""
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.exceptions import ValidationError, ErrorDetail

from ..models import CustomUser, SpecialistSchedule
from ..serializers.schedule_serializers import SpecialistScheduleSerializer
from ..services.customuser_services import add_user_to_group_specialist
from ..utils import generate_working_time_intervals


class SpecialistScheduleModelTest(TestCase):
    """Class SpecialistScheduleModelTest for testing SpecialistSchedule model."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.user_data = {
            "email": "specialist@com.ua",
            "first_name": "Fn",
            "last_name": "Ln"
        }
        self.specialist = CustomUser.objects.create_user(**self.user_data)
        add_user_to_group_specialist(self.specialist)

        self.working_time = generate_working_time_intervals("10:00", "20:00")

    def test_create_schedule_valid_data(self):
        """Test for creating schedule with valid data."""
        schedule = SpecialistSchedule.objects.create(
            specialist=self.specialist,
            working_time=self.working_time
        )

        self.assertEqual(schedule.specialist, self.specialist)
        self.assertEqual(schedule.working_time, self.working_time)
        self.assertIsInstance(schedule.working_time, dict)

    def test_create_schedule_not_specialist_error(self):
        """Test for creating schedule user is not specialist."""
        self.user_data.update(dict(email="user@com.ua"))
        user = CustomUser.objects.create_user(**self.user_data)
        schedule = SpecialistSchedule.objects.create(specialist=user,
                                                     working_time=self.working_time)

        full_name = user.get_full_name()

        with self.assertRaises(ValidationError) as ex:
            schedule.full_clean()
        message = ex.exception.args[0]
        self.assertEqual(message, {
            f"{full_name}": ErrorDetail(
                string=f"{full_name} should be specialist.", code="invalid"
            )
        })

    def test_create_schedule_working_time_invalid(self):
        """Test for creating schedule user is not specialist."""
        working_time = None
        with self.assertRaises(IntegrityError):
            SpecialistSchedule.objects.create(specialist=self.specialist,
                                              working_time=working_time)


class SpecialistScheduleSerializerTest(TestCase):
    """Class SpecialistScheduleSerializerTest for testing SpecialistSchedule serializers."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.user_data = {
            "email": "specialist@com.ua",
            "first_name": "Fn",
            "last_name": "Ln"
        }
        self.specialist = CustomUser.objects.create_user(**self.user_data)
        add_user_to_group_specialist(self.specialist)

        self.working_time = generate_working_time_intervals("10:00", "20:00")

        self.valid_data = {
            "specialist": self.specialist.id,
            "working_time": self.working_time
        }
        self.serializer = SpecialistScheduleSerializer(data=self.valid_data)

    def test_serialize_valid_data(self):
        """Check serializer with valid data."""
        self.serializer.is_valid(raise_exception=True)

        self.assertEqual(
            self.serializer.validated_data["specialist"].id,
            self.valid_data["specialist"]
        )
        self.assertEqual(
            self.serializer.validated_data["working_time"],
            self.valid_data["working_time"]
        )

        schedule = self.serializer.save()
        self.assertEqual(
            self.serializer.data["specialist"],
            schedule.specialist.get_full_name()
        )

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
        self.schedule_serializer = SpecialistScheduleSerializer

    def test_serialize_valid_data(self):
        """Check serializer with valid data."""
        serializer = self.schedule_serializer(data=self.valid_data)
        serializer.is_valid(raise_exception=True)

        self.assertEqual(
            serializer.validated_data["specialist"].id,
            self.valid_data["specialist"]
        )
        self.assertEqual(
            serializer.validated_data["working_time"],
            self.valid_data["working_time"]
        )

        schedule = serializer.save()
        self.assertEqual(
            serializer.data["specialist"],
            schedule.specialist.get_full_name()
        )

    def test_working_time_match_time_format(self):
        """Check a working time has match format."""
        for invalid_time in ["invalid", "", "1030"]:
            with self.subTest(invalid_time=invalid_time):
                invalid_working_time = generate_working_time_intervals(
                    invalid_time, "20:00"
                )
                self.valid_data.update(dict(working_time=invalid_working_time))

                with self.assertRaises(ValidationError) as ex:
                    serializer = self.schedule_serializer(data=self.valid_data)
                    serializer.is_valid(raise_exception=True)

                message = ex.exception.args[0]

                self.assertEqual(message, {
                    "working_time": {
                        "Mon": [
                            ErrorDetail(
                                string=f"time data '{invalid_time}' does not match format '%H:%M'",
                                code="invalid"
                            )
                        ]
                    }
                })

    def test_working_start_end_times(self):
        """Check a working start and end times.

        End time should be more than start time.
        """
        invalid_interval = ["10:00", "9:00"]
        invalid_working_time = generate_working_time_intervals(*invalid_interval)
        self.valid_data.update(dict(working_time=invalid_working_time))

        with self.assertRaises(ValidationError) as ex:
            serializer = self.schedule_serializer(data=self.valid_data)
            serializer.is_valid(raise_exception=True)

        message = ex.exception.args[0]
        self.assertEqual(message, {
            "working_time": {
                "Mon": [
                    ErrorDetail(string="Start time should be more than end time.",
                                code="invalid")
                ]
            }
        })

    def test_schedule_start_end_times_minutes_error(self):
        """Test for schedule start and end times format.

        Time values must have minutes multiples of 5.
        """
        for minute in range(1, 5):
            invalid_time = f"10:0{minute}"
            invalid_working_time = generate_working_time_intervals(
                invalid_time, "11:00"
            )
            self.valid_data.update(dict(working_time=invalid_working_time))

            with self.subTest(time_value=minute):
                serializer = self.schedule_serializer(data=self.valid_data)
                with self.assertRaises(ValidationError) as ex:
                    serializer.is_valid(raise_exception=True)

                message = ex.exception.args[0]
                self.assertEqual(message, {
                    "working_time": {
                        f"{invalid_time}:00": [
                            ErrorDetail(
                                string="Time value must have zero"
                                       " seconds and minutes multiples of 5.",
                                code="invalid"
                            )
                        ]
                    }
                })

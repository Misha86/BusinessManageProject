"""The module includes tests for Schedule model, serializers and views."""

from datetime import datetime, timedelta

from api.factories.factories import (
    AppointmentFactory,
    CustomUserFactory,
    SpecialistFactory,
    SpecialistScheduleFactory,
)
from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import CustomUser
from ..serializers.schedule_serializers import SpecialistScheduleSerializer
from ..services.schedule_services import get_working_day
from ..utils import generate_working_time_intervals, time_to_string


class SpecialistScheduleModelTest(TestCase):
    """Class SpecialistScheduleModelTest for testing SpecialistSchedule model."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.schedule = SpecialistScheduleFactory

    def tearDown(self):
        """This method deletes all users and cleans avatars' data."""
        CustomUser.objects.all().delete()

    def test_create_schedule_valid_data(self):
        """Test for creating schedule with valid data."""
        specialist = SpecialistFactory()
        schedule = self.schedule(specialist=specialist)

        self.assertIsNone(schedule.full_clean())
        self.assertEqual(schedule.specialist, specialist)
        self.assertIsInstance(schedule.working_time, dict)

    def test_create_schedule_not_specialist_error(self):
        """Test for creating schedule user is not specialist."""
        user = CustomUserFactory()
        schedule = self.schedule(specialist=user)
        full_name = user.get_full_name()
        with self.assertRaises(ValidationError) as ex:
            schedule.full_clean()
        message = ex.exception.args[0]
        self.assertEqual(
            message, {"specialist": ErrorDetail(string=f"{full_name} should be specialist.", code="invalid")}
        )

    def test_create_schedule_working_time_invalid(self):
        """Test for creating schedule with invalid working time."""
        with self.assertRaises(IntegrityError):
            self.schedule(working_time_null=True)


class SpecialistScheduleSerializerTest(TestCase):
    """Class SpecialistScheduleSerializerTest for testing SpecialistSchedule serializers."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.specialist = SpecialistFactory()
        self.schedule_serializer = SpecialistScheduleSerializer
        self.get_data = lambda w: {"specialist": self.specialist.id, "working_time": w}

    def tearDown(self):
        """This method deletes all users and cleans avatars' data."""
        CustomUser.objects.all().delete()

    def test_serialize_valid_data(self):
        """Check serializer with valid data."""
        working_time = SpecialistScheduleFactory.build().working_time
        serializer = self.schedule_serializer(data=self.get_data(working_time))
        serializer.is_valid(raise_exception=True)

        self.assertEqual(serializer.validated_data["specialist"].id, self.specialist.id)
        self.assertEqual(serializer.validated_data["working_time"], working_time)

        schedule = serializer.save()
        self.assertEqual(serializer.data["specialist"], schedule.specialist.get_full_name())

    def test_working_time_match_time_format(self):
        """Check a working time has match format."""
        for invalid_time in ["invalid", "", "1030"]:
            with self.subTest(invalid_time=invalid_time):
                with self.assertRaises(ValidationError) as ex:
                    serializer = self.schedule_serializer(data=self.get_data({"Mon": [[invalid_time, "20:00"]]}))
                    serializer.is_valid(raise_exception=True)

                message = ex.exception.args[0]

                self.assertEqual(
                    message,
                    {
                        "working_time": {
                            "Mon": [
                                ErrorDetail(
                                    string=f"time data '{invalid_time}' does not match format '%H:%M'", code="invalid"
                                )
                            ]
                        }
                    },
                )

    def test_working_start_end_times(self):
        """Check a working start and end times.

        End time should be more than start time.
        """
        with self.assertRaises(ValidationError) as ex:
            serializer = self.schedule_serializer(data=self.get_data({"Mon": [["10:00", "9:00"]]}))
            serializer.is_valid(raise_exception=True)

        message = ex.exception.args[0]
        self.assertEqual(
            message,
            {"working_time": {"Mon": [ErrorDetail(string="Start time should be more than end time.", code="invalid")]}},
        )

    def test_schedule_start_end_times_minutes_error(self):
        """Test for schedule start and end times format.

        Time values must have minutes multiples of 5.
        """
        day = "Mon"
        for minute in range(1, 5):
            with self.subTest(time_value=minute):
                serializer = self.schedule_serializer(data=self.get_data({day: [[f"10:0{minute}", "11:00"]]}))
                with self.assertRaises(ValidationError) as ex:
                    serializer.is_valid(raise_exception=True)

                message = ex.exception.args[0]
                self.assertEqual(
                    message,
                    {
                        "working_time": {
                            day: [
                                ErrorDetail(
                                    string="Time value must have zero seconds and minutes multiples of 5.",
                                    code="invalid",
                                )
                            ]
                        }
                    },
                )


class SpecialistScheduleViewTest(APITestCase):
    """Class SpecialistScheduleViewTest for testing SpecialistSchedule views."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.working_time = generate_working_time_intervals("10:00", "20:00")
        self.spec_schedule_date_url = "api:specialist-schedule-date"

    def tearDown(self):
        """This method deletes all users and cleans avatars' data."""
        CustomUser.objects.all().delete()

    def test_get_all_schedules(self):
        """Test for getting all schedules."""
        SpecialistScheduleFactory.create_batch(3)
        response = self.client.get(reverse("api:schedules-list-create"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_get_specialist_schedule(self):
        """Test to get a specialist schedule."""
        specialist = SpecialistFactory(add_schedule=True)
        response = self.client.get(reverse("api:specialist-schedule", args=(specialist.id,)), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["working_time"], specialist.schedule.working_time)
        with self.assertRaises(KeyError):
            response.data["specialist"]

    def test_get_specialist_schedule_for_date(self):
        """Test to get a specialist schedule for concrete date."""
        appointment = AppointmentFactory()
        start_time = time_to_string(appointment.start_time)
        end_time = time_to_string(appointment.end_time)
        specialist = appointment.specialist
        working_date = appointment.start_time.date()
        working_day = get_working_day(specialist.schedule.working_time, working_date)[0]
        response = self.client.get(
            reverse(self.spec_schedule_date_url, kwargs={"s_id": specialist.id, "a_date": working_date}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "appointments_intervals": [[start_time, end_time]],
                "free_intervals": [[working_day[0], start_time], [end_time, working_day[1]]],
            },
        )

    def test_get_schedule_not_specialist(self):
        """Test to get schedule for concrete date when a user is not specialist."""
        user = CustomUserFactory()
        a_date = datetime.now().date() + timedelta(days=1)

        response = self.client.get(
            reverse(self.spec_schedule_date_url, kwargs={"s_id": user.id, "a_date": a_date}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_schedule_past_date_error(self):
        """Test to get schedule for past date."""
        a_date = datetime.now().date() - timedelta(days=2)
        specialist = SpecialistScheduleFactory().specialist

        response = self.client.get(
            reverse(self.spec_schedule_date_url, kwargs={"s_id": specialist.id, "a_date": a_date}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"detail": "You can't see schedule of the past days."})

    def test_get_schedule_not_working_day_error(self):
        """Test to get schedule for a specialist rest day."""
        specialist = SpecialistScheduleFactory(working_time={}).specialist

        response = self.client.get(
            reverse(self.spec_schedule_date_url, kwargs={"s_id": specialist.id, "a_date": datetime.now().date()}),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"detail": f"{specialist.get_full_name()} is not working on this day."})

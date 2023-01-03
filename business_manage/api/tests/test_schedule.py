"""The module includes tests for Schedule model, serializers and views."""

from datetime import datetime, timedelta
from django.db import IntegrityError
from django.test import TestCase
from django.utils.timezone import get_current_timezone
from rest_framework.exceptions import ValidationError, ErrorDetail

from ..models import CustomUser, SpecialistSchedule, Location, Appointment
from ..serializers.schedule_serializers import SpecialistScheduleSerializer
from ..services.customuser_services import add_user_to_group_specialist
from ..utils import generate_working_time_intervals, string_to_time, generate_working_time, time_to_string
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from api.factories.factories import (
    AdminFactory,
    LocationFactory,
    ManagerFactory,
    SpecialistFactory,
    SuperuserFactory,
CustomUserFactory,
SpecialistScheduleFactory
)


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


# class SpecialistScheduleSerializerTest(TestCase):
#     """Class SpecialistScheduleSerializerTest for testing SpecialistSchedule serializers."""
#
#     def setUp(self):
#         """This method adds needed info for tests."""
#         self.user_data = get_user_data()
#         self.specialist = CustomUser.objects.create_user(**self.user_data)
#         add_user_to_group_specialist(self.specialist)
#
#         self.working_time = generate_working_time_intervals("10:00", "20:00")
#
#         self.valid_data = {"specialist": self.specialist.id, "working_time": self.working_time}
#         self.schedule_serializer = SpecialistScheduleSerializer
#
#     def test_serialize_valid_data(self):
#         """Check serializer with valid data."""
#         serializer = self.schedule_serializer(data=self.valid_data)
#         serializer.is_valid(raise_exception=True)
#
#         self.assertEqual(serializer.validated_data["specialist"].id, self.valid_data["specialist"])
#         self.assertEqual(serializer.validated_data["working_time"], self.valid_data["working_time"])
#
#         schedule = serializer.save()
#         self.assertEqual(serializer.data["specialist"], schedule.specialist.get_full_name())
#
#     def test_working_time_match_time_format(self):
#         """Check a working time has match format."""
#         for invalid_time in ["invalid", "", "1030"]:
#             with self.subTest(invalid_time=invalid_time):
#                 invalid_working_time = generate_working_time_intervals(invalid_time, "20:00")
#                 self.valid_data.update(dict(working_time=invalid_working_time))
#
#                 with self.assertRaises(ValidationError) as ex:
#                     serializer = self.schedule_serializer(data=self.valid_data)
#                     serializer.is_valid(raise_exception=True)
#
#                 message = ex.exception.args[0]
#
#                 self.assertEqual(
#                     message,
#                     {
#                         "working_time": {
#                             "Mon": [
#                                 ErrorDetail(
#                                     string=f"time data '{invalid_time}' does not match format '%H:%M'", code="invalid"
#                                 )
#                             ]
#                         }
#                     },
#                 )
#
#     def test_working_start_end_times(self):
#         """Check a working start and end times.
#
#         End time should be more than start time.
#         """
#         invalid_interval = ["10:00", "9:00"]
#         invalid_working_time = generate_working_time_intervals(*invalid_interval)
#         self.valid_data.update(dict(working_time=invalid_working_time))
#
#         with self.assertRaises(ValidationError) as ex:
#             serializer = self.schedule_serializer(data=self.valid_data)
#             serializer.is_valid(raise_exception=True)
#
#         message = ex.exception.args[0]
#         self.assertEqual(
#             message,
#             {"working_time": {"Mon": [ErrorDetail(string="Start time should be more than end time.", code="invalid")]}},
#         )
#
#     def test_schedule_start_end_times_minutes_error(self):
#         """Test for schedule start and end times format.
#
#         Time values must have minutes multiples of 5.
#         """
#         for minute in range(1, 5):
#             invalid_time = f"10:0{minute}"
#             invalid_working_time = generate_working_time_intervals(invalid_time, "11:00")
#             self.valid_data.update(dict(working_time=invalid_working_time))
#
#             with self.subTest(time_value=minute):
#                 serializer = self.schedule_serializer(data=self.valid_data)
#                 with self.assertRaises(ValidationError) as ex:
#                     serializer.is_valid(raise_exception=True)
#
#                 message = ex.exception.args[0]
#                 self.assertEqual(
#                     message,
#                     {
#                         "working_time": {
#                             f"{invalid_time}:00": [
#                                 ErrorDetail(
#                                     string="Time value must have zero" " seconds and minutes multiples of 5.",
#                                     code="invalid",
#                                 )
#                             ]
#                         }
#                     },
#                 )
#
#
# class SpecialistScheduleViewTest(TestCase):
#     """Class SpecialistScheduleViewTest for testing SpecialistSchedule views."""
#
#     def setUp(self):
#         """This method adds needed info for tests."""
#         self.client = APIClient()
#
#         self.user_data = get_user_data()
#         self.specialist = CustomUser.objects.create_user(**self.user_data)
#         add_user_to_group_specialist(self.specialist)
#
#         self.working_time = generate_working_time_intervals("10:00", "20:00")
#
#         self.valid_data = {"specialist": self.specialist, "working_time": self.working_time}
#         self.schedule = SpecialistSchedule.objects.create(**self.valid_data)
#         self.spec_schedule_date_url = "api:specialist-schedule-date"
#
#     def test_get_all_schedules(self):
#         """Test for getting all schedules."""
#         response = self.client.get(reverse("api:schedules-list-create"), format="json")
#         results = response.data["results"]
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(results), 1)
#         self.assertEqual(results[0]["specialist"], self.schedule.specialist.get_full_name())
#
#     def test_get_specialist_schedule(self):
#         """Test to get a specialist schedule."""
#         response = self.client.get(reverse("api:specialist-schedule", args=(self.specialist.id,)), format="json")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["working_time"], self.schedule.working_time)
#         with self.assertRaises(KeyError):
#             response.data["specialist"]
#
#     def test_get_specialist_schedule_for_date(self):
#         """Test to get a specialist schedule for concrete date."""
#         valid_data = get_appointment_data(self.specialist)
#         appointment = Appointment.objects.create(**valid_data)
#         start_time = appointment.start_time
#         end_time = appointment.end_time
#
#         response = self.client.get(
#             reverse(self.spec_schedule_date_url, kwargs={"s_id": self.specialist.id, "a_date": start_time.date()}),
#             format="json",
#         )
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             response.json(),
#             {
#                 "appointments intervals": [[f"{time_to_string(start_time)}", f"{time_to_string(end_time)}"]],
#                 "free intervals": [["10:00", "12:15"], ["12:35", "20:00"]],
#             },
#         )
#
#     def test_get_schedule_not_specialist(self):
#         """Test to get schedule for concrete date when a user is not specialist."""
#         self.user_data.update(dict(email="user@com.ua"))
#         user = CustomUser.objects.create_user(**self.user_data)
#         a_date = datetime.now().date() + timedelta(days=1)
#
#         response = self.client.get(
#             reverse(self.spec_schedule_date_url, kwargs={"s_id": user.id, "a_date": a_date}), format="json"
#         )
#         full_name = self.specialist.get_full_name()
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.data, {"detail": f"User {full_name} is not specialist."})
#
#     def test_get_schedule_past_date_error(self):
#         """Test to get schedule for past date."""
#         a_date = datetime.now().date() - timedelta(days=2)
#
#         response = self.client.get(
#             reverse(self.spec_schedule_date_url, kwargs={"s_id": self.specialist.id, "a_date": a_date}), format="json"
#         )
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.data, {"detail": "You can't see schedule of the past days."})
#
#     def test_get_schedule_not_working_day_error(self):
#         """Test to get schedule for a specialist rest day."""
#         a_date = datetime.now().date() + timedelta(days=2)
#         working_time = generate_working_time_intervals()
#         self.schedule.working_time = working_time
#         self.schedule.save()
#
#         response = self.client.get(
#             reverse(self.spec_schedule_date_url, kwargs={"s_id": self.specialist.id, "a_date": a_date}), format="json"
#         )
#         full_name = self.specialist.get_full_name()
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.data, {"detail": f"{full_name} is not working on this day"})

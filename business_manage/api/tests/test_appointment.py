"""The module includes tests for Appointment model, serializers and views."""

from django.test import TestCase
from django.utils.timezone import datetime, get_current_timezone, make_aware, timedelta
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ..models import Appointment, CustomUser, Location, SpecialistSchedule
from ..serializers.appointment_serializers import AppointmentSerializer
from ..services.customuser_services import add_user_to_group_specialist
from ..utils import generate_working_time_intervals, string_to_time
from api.factories.factories import (
    AppointmentFactory,
    CustomUserFactory,
    SpecialistFactory,
    SpecialistScheduleFactory,
    LocationFactory
)
from rest_framework.test import APITestCase
from django.utils import timezone


# def get_data_for_tests():
#     """Set up data for tests."""
#     user_data = {"email": "specialist@com.ua", "first_name": "Fn", "last_name": "Ln"}
#     specialist = CustomUser.objects.create_user(**user_data)
#     add_user_to_group_specialist(specialist)
#
#     user_data |= dict(email="user@com.ua")
#
#     user = CustomUser.objects.create_user(**user_data)
#
#     location = Location.objects.create(name="office #1", working_time={})
#
#     start_time = datetime.combine(
#         datetime.now().date() + timedelta(days=1), string_to_time("09:15"), tzinfo=get_current_timezone()
#     )
#     duration = timedelta(minutes=20)
#
#     working_time = generate_working_time_intervals(
#         start_time.strftime("%H:%M"), (start_time + duration).strftime("%H:%M")
#     )
#     SpecialistSchedule.objects.create(specialist=specialist, working_time=working_time)
#
#     # valid data for models and views tests
#     valid_data = {
#         "start_time": start_time,
#         "duration": duration,
#         "specialist": specialist,
#         "location": location,
#         "customer_firstname": "customer_firstname",
#         "customer_lastname": "customer_lastname",
#         "customer_email": "customer@com.ua",
#         "note": "",
#         "is_active": True,
#     }
#     # valid data for serializers tests
#     valid_data_s = {**valid_data, "specialist": specialist.pk, "location": location.pk}
#     return user_data, specialist, user, location, valid_data, valid_data_s


class AppointmentModelTest(TestCase):
    """Class AppointmentModelTest for testing Appointment model."""

    def setUp(self):
        """This method adds needed info for tests."""

        self.appointment = AppointmentFactory

    def tearDown(self):
        """This method deletes all users and cleans avatars' data."""
        CustomUser.objects.all().delete()

    def test_create_appointment_valid_data(self):
        """Test for creating appointment with valid data."""
        location = LocationFactory()
        specialist = SpecialistFactory()
        appointment = self.appointment(location=location, specialist=specialist)

        self.assertIsNone(appointment.full_clean())
        self.assertEqual(appointment.location, location)
        self.assertEqual(appointment.specialist, specialist)
        self.assertIsNotNone(appointment.customer_email)

    def test_appointment_end_time(self):
        """Test for appointment end time.

        End time should be more as start time.
        """
        appointment = self.appointment()
        start_time = appointment.start_time
        duration = appointment.duration
        end_time = start_time + duration
        self.assertEqual(appointment.end_time, end_time)
        self.assertGreater(appointment.end_time, start_time)

    def test_appointment_user_specialist(self):
        """Test for appointment specialist.

        User should be a specialist.
        """
        self.assertTrue(self.appointment().specialist.groups.filter(name="Specialist"))

    def test_appointment_user_not_specialist_error(self):
        """Test for appointment specialist validator.

        User should be a specialist (check by validator validate_specialist).
        """
        with self.assertRaises(ValidationError) as ex:
            appointment = self.appointment(specialist=CustomUserFactory())
            full_name = appointment.specialist.get_full_name().title()
            appointment.full_clean()
        message = ex.exception.args[0]
        self.assertEqual(message, {"specialist": f"{full_name} should be specialist."})

    def test_appointment_start_end_times_seconds_error(self):
        """Test for appointment start and end times format.

        Time values must have zero seconds.
        """
        seconds = make_aware(timezone.datetime.strptime("21/11/2023 15:10:10", "%d/%m/%Y %H:%M:%S"))

        with self.assertRaises(ValidationError) as ex:
            self.appointment(start_time=seconds).full_clean()

        message = ex.exception.args[0]
        self.assertEqual(
            message,
            "Time value must have zero seconds and minutes multiples of 5."
        )

    def test_appointment_duration_minutes_error(self):
        """Test for appointment duration format.

        Duration value must have minutes multiples of 5.
        """
        for i in range(1, 5):
            with self.subTest(invalid_minutes=i):
                with self.assertRaises(ValidationError) as ex:
                    self.appointment(duration=timedelta(minutes=int(f"1{i}"))).full_clean(exclude=["end_time"])

                message = ex.exception.args[0]
                self.assertEqual(message, "Duration value must have zero seconds and minutes multiples of 5.")

    def test_appointment_duration_seconds_error(self):
        """Test for appointment duration format.

        Duration value must have zero seconds..
        """
        with self.assertRaises(ValidationError) as ex:
            self.appointment(duration=timedelta(minutes=10, seconds=10)).full_clean(exclude=["end_time"])

        message = ex.exception.args[0]
        self.assertEqual(message, "Duration value must have zero seconds and minutes multiples of 5.")

    def test_appointment_time_range_past_datetime_error(self):
        """Test for appointment start and end times format.

        DateTime values should have current or future date.
        """
        invalid_date = make_aware(datetime.strptime("21/11/1900 11:10:00", "%d/%m/%Y %H:%M:%S"))
        with self.assertRaises(ValidationError) as ex:
            self.appointment(start_time=invalid_date).full_clean()

        message = ex.exception.args[0]
        self.assertEqual(
            message, f"DateTime value should have future datetime.")

    def test_appointment_method_mark_as_completed(self):
        """Test for appointment mark_as_completed method."""
        appointment = self.appointment()
        appointment.mark_as_completed()

        self.assertFalse(appointment.is_active)


class AppointmentSerializerTest(TestCase):
    """Class LocationSerializerTest for testing Location serializers."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.factory = SpecialistFactory(add_schedule=True)
        self.specialist = self.factory
        self.location = LocationFactory()
        fake_data = AppointmentFactory.build()
        self.valid_data = {"start_time": fake_data.start_time, "specialist": self.specialist.id,
                           "location": self.location.id,
                           "duration": fake_data.duration, "customer_email": fake_data.customer_email,
                           "customer_firstname": fake_data.customer_firstname,
                           "customer_lastname": fake_data.customer_lastname, }

        self.serializer = AppointmentSerializer(data=self.valid_data)

    def tearDown(self):
        """This method deletes all users and cleans avatars' data."""
        CustomUser.objects.all().delete()

    def test_serialize_valid_data(self):
        """Check serializer with valid data."""
        self.serializer.is_valid(raise_exception=True)

        self.assertEqual(self.serializer.validated_data["start_time"], self.valid_data["start_time"])
        self.assertEqual(self.serializer.validated_data["duration"], self.valid_data["duration"])
        self.assertEqual(self.serializer.validated_data["customer_firstname"], self.valid_data["customer_firstname"])
        self.assertEqual(self.serializer.validated_data["customer_lastname"], self.valid_data["customer_lastname"])
        self.assertEqual(self.serializer.validated_data["customer_email"], self.valid_data["customer_email"])

    def test_serialize_validate_method_success(self):
        """Check serializer validate method when data is valid."""
        self.serializer.is_valid(raise_exception=True)

        appointment = self.serializer.save()
        end_time = appointment.start_time + appointment.duration
        self.assertEqual(appointment.end_time, end_time)

    def test_serialize_validate_method_invalid_duration(self):
        """Check serializer validate method with invalid duration."""
        invalid_duration = timedelta(days=-1)
        self.valid_data.update(dict(duration=invalid_duration))

        with self.assertRaises(ValidationError) as ex:
            self.serializer.is_valid(raise_exception=True)

        message = ex.exception.args[0]
        self.assertEqual(
            message, {"start_time": [ErrorDetail(string="Start time should be more than end time.", code="invalid")]}
        )

    def test_serialize_specialist_schedule_none(self):
        """Check serializer when specialist doesn't have schedule."""
        specialist = SpecialistFactory()
        self.valid_data.update(dict(specialist=specialist.id))

        with self.assertRaises(ValidationError) as ex:
            self.serializer.is_valid(raise_exception=True)

        message = ex.exception.args[0]
        self.assertEqual(message,
                         {"specialist": [ErrorDetail(string="\"2\" is not a valid choice.", code="invalid_choice")]})

    def test_serialize_invalid_start_time(self):
        """Check serializer validate method with invalid start time."""
        invalid_start_time = datetime.combine(
            datetime.now().date() + timedelta(days=-1), string_to_time("09:15"), tzinfo=get_current_timezone()
        )
        self.valid_data.update(dict(start_time=invalid_start_time))

        with self.assertRaises(ValidationError) as ex:
            self.serializer.is_valid(raise_exception=True)

        message = ex.exception.args[0]
        self.assertEqual(
            message,
            {"start_time": [ErrorDetail(string="DateTime value should have future datetime.", code="invalid")]},
        )

    def test_serialize_start_time_is_none(self):
        """Check serializer validate method with null start time."""
        invalid_start_time = None
        self.valid_data.update(dict(start_time=invalid_start_time))

        with self.assertRaises(ValidationError) as ex:
            self.serializer.is_valid(raise_exception=True)

        message = ex.exception.args[0]
        self.assertEqual(message, {"start_time": [ErrorDetail(string="This field may not be null.", code="null")]})

    def test_to_representation_method(self):
        """Check serializer a to_representation method."""
        self.serializer.is_valid(raise_exception=True)

        self.serializer.save()
        specialist_full_name = self.specialist.get_full_name()

        self.assertEqual(self.serializer.data["specialist"], specialist_full_name)
        self.assertEqual(self.serializer.data["location"], self.location.name)

# class LocationViewTest(TestCase):
#     """Class LocationViewTest for testing Location view."""
#
#     def setUp(self):
#         """This method adds needed info for tests."""
#         self.client = APIClient()
#
#         self.create_ap_url = "api:appointments-list-create"
#
#         data_for_tests = get_data_for_tests()
#         (self.user_data, self.specialist, self.user, self.location, self.valid_data, _) = data_for_tests
#
#     def test_get_all_appointments(self):
#         """Test for getting all appointments."""
#         appointment = Appointment.objects.create(**self.valid_data)
#         response = self.client.get(reverse(self.create_ap_url), format="json")
#         results = response.data["results"]
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(results), 1)
#         self.assertEqual(results[0]["specialist"], appointment.specialist.get_full_name())
#         self.assertEqual(results[0]["location"], appointment.location.name)
#
#     def test_create_appointment_by_specialist_fail(self):
#         """Test for creating appointment by specialist is forbidden."""
#         self.client.force_authenticate(self.specialist)
#
#         self.valid_data.update(dict(specialist=self.specialist.id, location=self.location.id))
#
#         response = self.client.post(reverse(self.create_ap_url), self.valid_data, format="json")
#         self.assertEqual(response.status_code, 403)
#
#     def test_create_appointment_by_admin(self):
#         """Test for creating appointment by admin."""
#         self.user_data.update(dict(email="admin@com.ua"))
#         admin = CustomUser.objects.create_admin(password="password", **self.user_data)
#
#         self.client.force_authenticate(admin)
#
#         self.valid_data.update(dict(specialist=self.specialist.id, location=self.location.id))
#
#         response = self.client.post(reverse(self.create_ap_url), self.valid_data, format="json")
#         self.assertEqual(response.status_code, 201)
#
#     def test_create_appointment_by_manager_fail(self):
#         """Test for creating appointment by manager is forbidden."""
#         self.user_data.update(dict(email="manager@com.ua"))
#         manager = CustomUser.objects.create_manager(password="password", **self.user_data)
#
#         self.client.force_authenticate(manager)
#
#         self.valid_data.update(dict(specialist=self.specialist.id, location=self.location.id))
#
#         response = self.client.post(reverse(self.create_ap_url), self.valid_data, format="json")
#         self.assertEqual(response.status_code, 403)
#
#     def test_create_appointment_by_superuser(self):
#         """Test for creating appointment by superuser."""
#         self.user_data.update(dict(email="superuser@com.ua"))
#         superuser = CustomUser.objects.create_superuser(password="password", **self.user_data)
#
#         self.client.force_authenticate(superuser)
#
#         self.valid_data.update(dict(specialist=self.specialist.id, location=self.location.id))
#
#         response = self.client.post(reverse(self.create_ap_url), self.valid_data, format="json")
#         self.assertEqual(response.status_code, 201)
#
#     def test_create_appointment_not_specialist_schedule_error(self):
#         """Test for creating appointment with specialist without schedule (Bad request 400)."""
#         self.user_data.update(dict(email="admin@com.ua"))
#         admin = CustomUser.objects.create_admin(password="password", **self.user_data)
#
#         self.client.force_authenticate(admin)
#
#         self.specialist.schedule.delete()
#
#         self.valid_data.update(dict(specialist=self.specialist.id, location=self.location.id))
#
#         response = self.client.post(reverse(self.create_ap_url), self.valid_data, format="json")
#         self.assertEqual(response.status_code, 40

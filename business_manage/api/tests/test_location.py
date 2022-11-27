"""The module includes tests for Location model, serializers and views."""

from django.db import IntegrityError
from django.test import TestCase
from rest_framework.exceptions import ValidationError, ErrorDetail
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ..models import Location, CustomUser
from ..serializers.location_serializers import LocationSerializer
from ..services.customuser_services import add_user_to_group_specialist
from ..utils import generate_working_time


class LocationModelTest(TestCase):
    """Class LocationModelTest for testing Location models."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.valid_data = {
            "name": "LName",
            "address": "234 New st.",
            "working_time": generate_working_time(),
        }
        self.location = Location.objects.create(**self.valid_data)

    def test_create_location_valid_data(self):
        """Test for creating location with valid data."""
        self.assertEqual(self.location.name, self.valid_data.get("name"))
        self.assertEqual(self.location.address, self.valid_data.get("address"))
        self.assertEqual(self.location.working_time, self.valid_data.get("working_time"))

    def test_location_name_uniqe(self):
        """Test for creating location with uniqe name."""
        with self.assertRaises(IntegrityError) as ex:
            Location.objects.create(**self.valid_data)
        message = ex.exception
        self.assertEqual(str(message), "UNIQUE constraint failed: api_location.name")

    def test_location_working_day_error(self):
        """Test for location working time field.

        Working days must be named such names [Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        """
        invalid_data = "Invalid"
        self.valid_data.update(dict(working_time={invalid_data: ["10:20", "11:20"]},
                                    name="Name"))

        location = Location.objects.create(**self.valid_data)

        with self.assertRaises(ValidationError) as ex:
            location.full_clean()

        message = ex.exception.args[0]
        self.assertEqual(message, {
            f"{invalid_data}":
                "Day name should be one of these ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']."
        })


class LocationSerializerTest(TestCase):
    """Class LocationSerializerTest for testing Location serializers."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.l_serializer = LocationSerializer
        working_time = generate_working_time("10:30", "10:50")
        self.valid_data = {
            "name": "office #1",
            "address": "234 New st.",
            "working_time": working_time
        }

    def test_serialize_valid_data(self):
        """Check serializer with valid data."""
        serializer = self.l_serializer(data=self.valid_data)

        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.validated_data["name"], self.valid_data["name"])
        self.assertEqual(serializer.validated_data["address"], self.valid_data["address"])
        self.assertEqual(serializer.validated_data["working_time"], self.valid_data["working_time"])

    def test_serialize_invalid_working_time_minutes(self):
        """Check serializer with invalid working time when minutes don't multiples of 5."""
        for i in range(1, 5):
            invalid_time = f"10:5{i}"
            self.valid_data.update(dict(working_time={"Mon": ["10:30", invalid_time]}))
            with self.subTest(i=i):
                serializer = self.l_serializer(data=self.valid_data)
                with self.assertRaises(ValidationError) as ex:
                    serializer.is_valid(raise_exception=True)
                message = ex.exception.args[0]
                self.assertEqual(
                    message,
                    {
                        "working_time": {
                            f"{invalid_time}:00": [
                                ErrorDetail(
                                    string="Time value must have zero seconds and "
                                           "minutes multiples of 5.",
                                    code="invalid"
                                )
                            ]
                        }
                    }
                )

    def test_serialize_invalid_working_time_seconds_exist(self):
        """Check serializer with invalid working time when seconds exist."""
        invalid_time = "10:50:10"
        self.valid_data.update(dict(working_time={"Mon": ["10:30", invalid_time]}))
        serializer = self.l_serializer(data=self.valid_data)

        with self.assertRaises(ValidationError) as ex:
            serializer.is_valid(raise_exception=True)
        message = ex.exception.args[0]
        self.assertEqual(
            message,
            {
                "working_time": {
                    "Mon": [
                        ErrorDetail(string="unconverted data remains: :10", code="invalid")
                    ]
                }
            }
        )

    def test_serialize_invalid_working_time_range(self):
        """Invalid time range.

        Check serializer with invalid working time when start time
        more or equal than end time.
        """
        start_time = "10:50"
        invalid_end_time = "10:40"
        for invalid_time_range in [invalid_end_time, start_time]:
            self.valid_data.update(dict(working_time={"Mon": [start_time, invalid_end_time]}))

            with self.subTest(invalid_time_range=invalid_time_range):
                serializer = self.l_serializer(data=self.valid_data)

                with self.assertRaises(ValidationError) as ex:
                    serializer.is_valid(raise_exception=True)

                message = ex.exception.args[0]
                self.assertEqual(
                    message,
                    {
                        "working_time": {
                            "Mon": [
                                ErrorDetail(string="Start time should be more than end time.",
                                            code="invalid")
                            ]
                        }
                    }
                )

    def test_serialize_invalid_working_time_not_end_time(self):
        """Check serializer with invalid working time when end time doesn't exist."""
        self.valid_data.update(dict(working_time={"Mon": ["10:40"]}))

        serializer = self.l_serializer(data=self.valid_data)

        with self.assertRaises(ValidationError) as ex:
            serializer.is_valid(raise_exception=True)
        message = ex.exception.args[0]
        self.assertEqual(
            message,
            {
                "working_time": {
                    "Mon": [
                        ErrorDetail(
                            string="Time range should be contain start and "
                                   "end time together or empty range.", code="invalid"
                        )
                    ]
                }
            }
        )

    def test_serialize_invalid_working_time_time_is_empty_string(self):
        """Invalid time range.

        Check serializer with invalid working time when start time or
        end time is empty string.
        """
        for invalid_time_range in [["", "10:40"], ["10:40", ""]]:
            self.valid_data.update(dict(working_time={"Mon": invalid_time_range}))

            with self.subTest(invalid_time_range=invalid_time_range):
                serializer = self.l_serializer(data=self.valid_data)

                with self.assertRaises(ValidationError) as ex:
                    serializer.is_valid(raise_exception=True)
                message = ex.exception.args[0]

                self.assertEqual(
                    message,
                    {
                        "working_time": {
                            "Mon": [
                                ErrorDetail(
                                    string="time data '' does not match format '%H:%M'",
                                    code="invalid"
                                )
                            ]
                        }
                    }
                )


class LocationViewTest(TestCase):
    """Class LocationViewTest for testing Location view."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.client = APIClient()
        self.user = CustomUser.objects
        self.valid_data = {
            "name": "office #1",
            "address": "234 New st.",
            "working_time": {
                "Mon": ["10:30", "10:50"],
                "Tue": ["10:30", "10:50"],
                "Wed": ["10:30", "10:50"],
                "Thu": ["10:30", "10:50"],
                "Fri": ["10:30", "10:50"],
                "Sat": [],
                "Sun": []
            }
        }
        self.user_data = {
            "password": "password",
            "email": "user@com.ua",
            "first_name": "first_name",
            "last_name": "last_name"
        }

    def test_get_all_locations(self):
        """Test for getting all locations."""
        location = Location.objects.create(**self.valid_data)
        response = self.client.get(reverse("api:locations-list-create"), format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], location.name)

    def test_create_location_by_specialist_fail(self):
        """Test for creating location by specialist is forbidden."""
        specialist = self.user.create_user(**self.user_data)
        add_user_to_group_specialist(specialist)
        self.client.force_authenticate(specialist)
        response = self.client.post(reverse("api:locations-list-create"),
                                    self.valid_data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_create_location_by_admin_fail(self):
        """Test for creating location by admin is forbidden."""
        admin = self.user.create_admin(**self.user_data)
        self.client.force_authenticate(admin)
        response = self.client.post(reverse("api:locations-list-create"),
                                    self.valid_data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_create_location_by_manager(self):
        """Test for creating location by manager is allowed."""
        manager = self.user.create_manager(**self.user_data)
        self.client.force_authenticate(manager)
        response = self.client.post(reverse("api:locations-list-create"),
                                    self.valid_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_location_by_superuser(self):
        """Test for creating location by manager is allowed."""
        superuser = self.user.create_superuser(**self.user_data)
        self.client.force_authenticate(superuser)
        response = self.client.post(reverse("api:locations-list-create"),
                                    self.valid_data, format="json")
        self.assertEqual(response.status_code, 201)

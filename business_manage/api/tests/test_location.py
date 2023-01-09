"""The module includes tests for Location model, serializers and views."""

from api.factories.factories import (
    AdminFactory,
    LocationFactory,
    ManagerFactory,
    SpecialistFactory,
    SuperuserFactory,
)
from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import CustomUser, Location
from ..serializers.location_serializers import LocationSerializer


class LocationModelTest(TestCase):
    """Class LocationModelTest for testing Location models."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.location = LocationFactory(__sequence=0)

    def test_create_location_valid_data(self):
        """Test for creating location with valid data."""
        self.assertIsNone(self.location.full_clean())
        self.assertEqual(self.location.name, "Location_0")

    def test_location_name_unique(self):
        """Test for creating location with unique name."""
        with self.assertRaises(IntegrityError) as ex:
            Location.objects.create(name=self.location.name)
        message = ex.exception
        self.assertEqual(str(message), "UNIQUE constraint failed: api_location.name")

    def test_location_working_day_error(self):
        """Test for location working time field.

        Working days must be named such names [Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        """
        location = LocationFactory.build(working_time={"Invalid Day": ["10:20", "11:20"]})

        with self.assertRaises(ValidationError) as ex:
            location.full_clean()

        message = ex.exception.args[0]

        self.assertEqual(message, "Day name should be one of these ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].")

    def test_repr_method(self):
        """Test __repr__ method."""
        location = LocationFactory()
        self.assertEqual(repr(location), f"{location.__class__.__name__}(id={location.id})")

class LocationSerializerTest(TestCase):
    """Class LocationSerializerTest for testing Location serializers."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.l_serializer = LocationSerializer
        self.build = LocationFactory.build

    def test_serialize_valid_data(self):
        """Check serializer with valid data."""
        valid_data = self.build().__dict__
        serializer = self.l_serializer(data=valid_data)

        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.validated_data["name"], valid_data["name"])
        self.assertEqual(serializer.validated_data["address"], valid_data["address"])
        self.assertEqual(serializer.validated_data["working_time"], valid_data["working_time"])

    def test_serialize_invalid_working_time_minutes(self):
        """Check serializer with invalid working time when minutes don't multiples of 5."""
        for i in range(1, 5):
            invalid_time = f"10:5{i}"
            invalid_data = self.build(working_time={"Mon": ["10:30", invalid_time]}).__dict__

            with self.subTest(i=i):
                serializer = self.l_serializer(data=invalid_data)

                with self.assertRaises(ValidationError) as ex:
                    serializer.is_valid(raise_exception=True)

                message = ex.exception.args[0]
                self.assertEqual(
                    message,
                    {
                        "working_time": {
                            "Mon": [
                                ErrorDetail(
                                    string="Time value must have zero seconds and " "minutes multiples of 5.",
                                    code="invalid",
                                )
                            ]
                        }
                    },
                )

    def test_serialize_invalid_working_time_seconds_exist(self):
        """Check serializer with invalid working time when seconds exist."""
        invalid_time = "10:50:10"
        invalid_data = self.build(working_time={"Mon": ["10:30", invalid_time]}).__dict__
        serializer = self.l_serializer(data=invalid_data)

        with self.assertRaises(ValidationError) as ex:
            serializer.is_valid(raise_exception=True)

        message = ex.exception.args[0]
        self.assertEqual(
            message, {"working_time": {"Mon": [ErrorDetail(string="unconverted data remains: :10", code="invalid")]}}
        )

    def test_serialize_invalid_working_time_range(self):
        """Invalid time range.

        Check serializer with invalid working time when start time
        more or equal than end time.
        """
        start_time = "10:50"
        invalid_end_time = "10:40"
        for invalid_time_range in [invalid_end_time, start_time]:
            invalid_data = self.build(working_time={"Mon": [start_time, invalid_end_time]}).__dict__
            with self.subTest(invalid_time_range=invalid_time_range):
                serializer = self.l_serializer(data=invalid_data)

                with self.assertRaises(ValidationError) as ex:
                    serializer.is_valid(raise_exception=True)

                message = ex.exception.args[0]
                self.assertEqual(
                    message,
                    {
                        "working_time": {
                            "Mon": [ErrorDetail(string="Start time should be more than end time.", code="invalid")]
                        }
                    },
                )

    def test_serialize_invalid_working_time_not_end_time(self):
        """Check serializer with invalid working time when end time doesn't exist."""
        invalid_data = self.build(working_time={"Mon": ["10:40"]}).__dict__

        serializer = self.l_serializer(data=invalid_data)

        with self.assertRaises(ValidationError) as ex:
            serializer.is_valid(raise_exception=True)
        message = ex.exception.args[0]
        self.assertEqual(
            message,
            {
                "working_time": {
                    "Mon": [
                        ErrorDetail(
                            string="Time range should be contain start and end time together or empty range.",
                            code="invalid",
                        )
                    ]
                }
            },
        )

    def test_serialize_invalid_working_time_time_is_empty_string(self):
        """Invalid time range.

        Check serializer with invalid working time when start time or
        end time is empty string.
        """
        for invalid_time_range in [["", "10:40"], ["10:40", ""]]:
            invalid_data = self.build(working_time={"Mon": invalid_time_range}).__dict__

            with self.subTest(invalid_time_range=invalid_time_range):
                serializer = self.l_serializer(data=invalid_data)

                with self.assertRaises(ValidationError) as ex:
                    serializer.is_valid(raise_exception=True)
                message = ex.exception.args[0]

                self.assertEqual(
                    message,
                    {
                        "working_time": {
                            "Mon": [ErrorDetail(string="time data '' does not match format '%H:%M'", code="invalid")]
                        }
                    },
                )


class LocationViewTest(APITestCase):
    """Class LocationViewTest for testing Location view."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.valid_data = {k: v for k, v in LocationFactory.build().__dict__.items() if k in ["name", "working_time"]}

        self.location_create_url = "api:locations-list-create"

    def tearDown(self):
        """This method deletes all users and cleans avatars' data."""
        CustomUser.objects.all().delete()

    def test_get_all_locations(self):
        """Test for getting all locations."""
        LocationFactory.create_batch(3)
        response = self.client.get(reverse(self.location_create_url), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_create_location_by_specialist_fail(self):
        """Test for creating location by specialist is forbidden."""
        self.client.force_authenticate(SpecialistFactory())
        response = self.client.post(reverse(self.location_create_url), self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_location_by_admin_fail(self):
        """Test for creating location by admin is forbidden."""
        self.client.force_authenticate(AdminFactory())
        response = self.client.post(reverse(self.location_create_url), self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_location_by_manager(self):
        """Test for creating location by manager is allowed."""
        self.client.force_authenticate(ManagerFactory())
        response = self.client.post(reverse(self.location_create_url), self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_location_by_superuser(self):
        """Test for creating location by manager is allowed."""
        self.client.force_authenticate(SuperuserFactory())
        response = self.client.post(reverse(self.location_create_url), self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

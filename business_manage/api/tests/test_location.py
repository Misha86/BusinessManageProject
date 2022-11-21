"""The module includes tests for Location model, serializers and views."""

from django.test import TestCase
from rest_framework.exceptions import ValidationError, ErrorDetail

from ..models import Location
from ..serializers.location_serializers import LocationSerializer
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

    def test_create_location_valid_data(self):
        """Test for creating location with  data."""
        location = Location.objects.create(**self.valid_data)

        self.assertEqual(location.name, self.valid_data.get("name"))
        self.assertEqual(location.address, self.valid_data.get("address"))
        self.assertEqual(location.working_time, self.valid_data.get("working_time"))


class LocationSerializerTest(TestCase):
    """Class LocationSerializerTest for testing Location serializers."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.l_serializer = LocationSerializer
        self.valid_data = {
            "name": "office #1",
            "address": "234 New st.",
            "working_time": {
                "mon": ["10:30", "10:50"],
                "tue": ["10:30", "10:50"],
                "wed": ["10:30", "10:50"],
                "thu": ["10:30", "10:50"],
                "fri": ["10:30", "10:50"],
                "sat": [],
                "sun": []
            }
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
            self.valid_data.update(dict(working_time={"mon": ["10:30", invalid_time]}))
            with self.subTest(i=i):
                serializer = self.l_serializer(data=self.valid_data)
                with self.assertRaises(ValidationError) as ex:
                    serializer.is_valid(raise_exception=True)
                message = ex.exception.args[0]
                self.assertEqual(
                    message,
                    {
                        "working_time": {
                            invalid_time: [
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
        self.valid_data.update(dict(working_time={"mon": ["10:30", invalid_time]}))
        serializer = self.l_serializer(data=self.valid_data)

        with self.assertRaises(ValidationError) as ex:
            serializer.is_valid(raise_exception=True)
        message = ex.exception.args[0]
        self.assertEqual(
            message,
            {
                "working_time": {
                    "mon": [
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
            self.valid_data.update(dict(working_time={"mon": [start_time, invalid_end_time]}))

            with self.subTest(invalid_time_range=invalid_time_range):
                serializer = self.l_serializer(data=self.valid_data)

                with self.assertRaises(ValidationError) as ex:
                    serializer.is_valid(raise_exception=True)

                message = ex.exception.args[0]
                self.assertEqual(
                    message,
                    {
                        "working_time": {
                            "mon": [
                                ErrorDetail(string="Start time should be more than end time.",
                                            code="invalid")
                            ]
                        }
                    }
                )

    def test_serialize_invalid_working_time_not_end_time(self):
        """Check serializer with invalid working time when end time doesn't exist."""
        self.valid_data.update(dict(working_time={"mon": ["10:40"]}))

        serializer = self.l_serializer(data=self.valid_data)

        with self.assertRaises(ValidationError) as ex:
            serializer.is_valid(raise_exception=True)
        message = ex.exception.args[0]
        self.assertEqual(
            message,
            {
                "working_time": {
                    "mon": [
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
            self.valid_data.update(dict(working_time={"mon": invalid_time_range}))

            with self.subTest(invalid_time_range=invalid_time_range):
                serializer = self.l_serializer(data=self.valid_data)

                with self.assertRaises(ValidationError) as ex:
                    serializer.is_valid(raise_exception=True)
                message = ex.exception.args[0]

                self.assertEqual(
                    message,
                    {
                        "working_time": {
                            "mon": [
                                ErrorDetail(
                                    string="time data '' does not match format '%H:%M'",
                                    code="invalid"
                                )
                            ]
                        }
                    }
                )

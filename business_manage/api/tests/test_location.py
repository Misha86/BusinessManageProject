"""The module includes tests for Location model, serializers and views."""

from django.test import TestCase
from ..models import Location
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

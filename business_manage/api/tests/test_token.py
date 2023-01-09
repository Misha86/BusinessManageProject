"""The module includes tests for Simple JWT."""

from api.factories.factories import (
    AdminFactory,
    AppointmentFactory,
    CustomUserFactory,
    LocationFactory,
    ManagerFactory,
    SpecialistFactory,
    SuperuserFactory,
)
from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import datetime, get_current_timezone, make_aware, timedelta
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import CustomUser
from ..serializers.appointment_serializers import AppointmentSerializer
from ..utils import string_to_time
from rest_framework_simplejwt.tokens import AccessToken


class SimpleJWTTest(APITestCase):
    """Class AppointmentViewTest for testing Simple JWT."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.create_tokens = "api:token_obtain_pair"

    def tearDown(self):
        """This method deletes all users and cleans avatars' data."""
        CustomUser.objects.all().delete()

    def test_create_token_admin(self):
        """Test for creating token by admin."""
        password = "0987654321"
        admin = AdminFactory(password=password)
        response = self.client.post(reverse(self.create_tokens), {"email": admin.email, "password": password},
                                    format="json")
        access_token = AccessToken(response.data["access"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"],
                         {'first_name': admin.first_name, 'last_name': admin.last_name, 'avatar': admin.avatar.url,
                          'groups': list(admin.groups.all().values_list("name", flat=True))})
        self.assertEqual(access_token['user_id'], admin.id)

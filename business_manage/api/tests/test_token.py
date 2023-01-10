"""The module includes tests for Simple JWT."""

from api.factories.factories import AdminFactory, ManagerFactory, SuperuserFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from ..models import CustomUser


class SimpleJWTTest(APITestCase):
    """Class AppointmentViewTest for testing Simple JWT."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.create_tokens = "api:token_obtain_pair"
        self.deactivate_token = "api:token_logout"

    def tearDown(self):
        """This method deletes all users and cleans avatars' data."""
        CustomUser.objects.all().delete()

    def check_token_creation(self, user, password=None):
        """Base test for creating token."""
        response = self.client.post(
            reverse(self.create_tokens), {"email": user.email, "password": password}, format="json"
        )
        access_token = AccessToken(response.data["access"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["user"],
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar": user.avatar.url,
                "groups": list(user.groups.all().values_list("name", flat=True)),
            },
        )
        self.assertEqual(access_token["user_id"], user.id)

    def test_create_token_admin(self):
        """Test for creating token by admin."""
        password = "0987654321"
        admin = AdminFactory(password=password)
        self.check_token_creation(admin, password)

    def test_create_token_manger(self):
        """Test for creating token by admin."""
        password = "0987654321"
        manager = ManagerFactory(password=password)
        self.check_token_creation(manager, password)

    def test_create_token_superuser(self):
        """Test for creating token by admin."""
        password = "0987654321"
        superuser = SuperuserFactory(password=password)
        self.check_token_creation(superuser, password)

    def test_blacklist_refresh_token(self):
        """Test logout user (blacklist refresh token)."""
        password = "0987654321"
        superuser = SuperuserFactory(password=password)
        response = self.client.post(reverse(self.create_tokens), {"email": superuser.email, "password": password})
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + response.data["access"])
        logout = self.client.post(reverse(self.deactivate_token), {"refresh": response.data["refresh"]})
        self.assertEqual(logout.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(logout.data)

    def test_blacklist_invalid_refresh_token(self):
        """Test logout user (blacklist invalid refresh token)."""
        password = "0987654321"
        superuser = AdminFactory(password=password)
        response = self.client.post(reverse(self.create_tokens), {"email": superuser.email, "password": password})
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + response.data["access"])
        logout = self.client.post(reverse(self.deactivate_token), {"refresh": "invalid_token"})
        self.assertEqual(logout.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(logout.data[0], "Token is invalid or expired")

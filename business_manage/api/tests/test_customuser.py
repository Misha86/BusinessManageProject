"""The module includes tests for CustomUser models, serializers and views."""

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from ..models import CustomUser
from ..serializers.customuser_serializers import SpecialistSerializer


class CustomUserModelTest(TestCase):
    """Class CustomUserModelTest for testing CustomUser models."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.groups = Group.objects.all()
        self.specialist_group = Group.objects.create(name="Specialist")
        self.user_data = {"first_name": "UserF",
                          "last_name": "UserL",
                          "patronymic": "",
                          "bio": "",
                          "email": "user@com.ua",
                          "password": "password"}

    def test_create_user(self):
        """Test for creating user."""
        user = CustomUser.objects.create_user(**self.user_data)

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.first_name, self.user_data.get("first_name"))
        self.assertEqual(user.last_name, self.user_data.get("last_name"))
        self.assertEqual(user.position, self.user_data.get("position", ""))
        self.assertEqual(user.email, self.user_data.get("email"))
        self.assertEqual(user.avatar.url, "/media/default_avatar.jpeg")
        self.assertTrue(check_password(self.user_data.get("password"), user.password))
        self.assertEqual(user.get_full_name(),
                         f"{self.user_data.get('first_name')} {self.user_data.get('last_name')}")
        self.assertEqual(user.get_short_name(), f"{self.user_data.get('first_name')}")

    def test_create_superuser(self):
        """Test for creating superuser."""
        super_user = CustomUser.objects.create_superuser(**self.user_data)

        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)
        self.assertEqual(super_user.position, "Owner")

    def test_create_superuser_without_password(self):
        """Test for creating superuser without password, should be error."""
        self.user_data.update(dict(password=None))
        with self.assertRaises(ValueError) as ex:
            CustomUser.objects.create_superuser(**self.user_data)
        message = ex.exception
        self.assertEqual(str(message), "Superuser must have an password.")

    def test_create_specialist(self):
        """Test for creating specialist."""
        specialist = CustomUser.objects.create_user(**self.user_data)
        self.specialist_group.user_set.add(specialist)

        self.assertFalse(specialist.is_staff)
        self.assertFalse(specialist.is_superuser)
        self.assertTrue(specialist.groups.filter(name="Specialist"))
        self.assertQuerysetEqual(specialist.groups.all(), self.groups)

    def test_create_specialist_without_password(self):
        """Test for creating specialist without password."""
        self.user_data.update(dict(password=None))
        specialist = CustomUser.objects.create_user(**self.user_data)
        self.specialist_group.user_set.add(specialist)
        self.assertEqual(specialist.password, "")

    def test_create_manager(self):
        """Test for creating manager."""
        manager = CustomUser.objects.create_manager(**self.user_data)

        self.assertFalse(manager.is_staff)
        self.assertFalse(manager.is_superuser)
        self.assertTrue(manager.is_manager)
        self.assertTrue(manager.groups.filter(name="Manager"))
        self.assertTrue(set(manager.groups.all()).intersection(set(self.groups)))

    def test_create_manager_without_password(self):
        """Test for creating manager without password, should be error."""
        self.user_data.update(dict(password=None))
        with self.assertRaises(ValueError) as ex:
            CustomUser.objects.create_manager(**self.user_data)
        message = ex.exception
        self.assertEqual(str(message), "Manager must have an password.")

    def test_create_admin(self):
        """Test for creating admin."""
        admin = CustomUser.objects.create_admin(**self.user_data)

        self.assertFalse(admin.is_staff)
        self.assertFalse(admin.is_superuser)
        self.assertTrue(admin.groups.filter(name="Admin"))
        self.assertTrue(admin.is_admin)
        self.assertTrue(set(admin.groups.all()).intersection(set(self.groups)))

    def test_create_admin_without_password(self):
        """Test for creating admin without password, should be error."""
        self.user_data.update(dict(password=None))
        with self.assertRaises(ValueError) as ex:
            CustomUser.objects.create_admin(**self.user_data)
        message = ex.exception
        self.assertEqual(str(message), "Admin must have an password.")


class CustomUserSerializerTest(TestCase):
    """Class CustomUserSerializerTest for testing CustomUser serializers."""

    valid_data = {"first_name": "UserF",
                  "last_name": "UserL",
                  "patronymic": "",
                  "position": "dentist",
                  "bio": "",
                  "is_active": True,
                  "email": "user@com.ua",
                  "password": "password"}

    ecxpect_data = {"email": "user@com.ua",
                    "first_name": "UserF",
                    "last_name": "UserL",
                    "patronymic": "",
                    "position": "dentist",
                    "bio": "",
                    "groups": [],
                    "avatar": "/media/default_avatar.jpeg",
                    "is_active": True}

    def setUp(self):
        """This method adds needed info for tests."""
        self.sp_serializer = SpecialistSerializer
        self.user = CustomUser.objects.create_user(**self.valid_data)
        self.groups = Group.objects.all()

    def test_valid_specialist_serializer(self):
        """Check serializer with valid data."""
        serializer = self.sp_serializer(instance=self.user)

        self.assertEqual(serializer.data, self.ecxpect_data)
        self.assertQuerysetEqual(self.groups.values_list("name", flat=True),
                                 self.ecxpect_data["groups"])

    def test_empty_serializer(self):
        """Check serializer without data."""
        serializer = self.sp_serializer()
        self.assertEqual(serializer.data,
                         {"email": "", "first_name": "", "last_name": "", "patronymic": "",
                          "position": "", "bio": "", "avatar": None, "is_active": True})

    def test_validate_none_data(self):
        """Check serializer with data equal None."""
        data = None
        serializer = self.sp_serializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {"non_field_errors": ["No data provided"]})
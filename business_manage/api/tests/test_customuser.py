"""The module includes tests for CustomUser models, serializers and views."""

import math

from api.factories import factories, fake_data
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import CustomUser
from ..serializers.customuser_serializers import SpecialistSerializer
from ..services.customuser_services import add_user_to_group_specialist
from ..utils import time_to_string
from rest_framework.exceptions import ErrorDetail


class CustomUserModelTest(TestCase):
    """Class CustomUserModelTest for testing CustomUser models."""

    def tearDown(self):
        """This method deletes all users and cleans avatars' data."""
        CustomUser.objects.all().delete()

    def test_create_user(self):
        """Test for creating user."""
        password = "0987654321"
        user = factories.CustomUserFactory(password=password, __sequence=0)

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.first_name)
        self.assertTrue(user.last_name)
        self.assertEqual(user.position, "")
        self.assertEqual(
            user.email,
            f"{user.first_name.lower()}.{user.last_name.lower()}_0@example.com",
        )
        self.assertEqual(user.avatar.url, f"/media/{user.avatar.name}")
        self.assertTrue(check_password(password, user.password))
        self.assertEqual(user.get_full_name(), f"{user.first_name} {user.last_name}".title())
        self.assertEqual(user.get_short_name(), user.first_name)

    def test_create_user_password_none(self):
        """Test for creating user without password."""
        user = factories.CustomUserFactory()
        self.assertEqual(user.password, "")

    def test_create_user_avatar_default(self):
        """Test for creating user with default avatar."""
        user = factories.CustomUserFactory(avatar=None)
        self.assertEqual(user.avatar.url, "/media/default_avatar.jpeg")

    def test_create_user_email_none_error(self):
        """Test for creating user without email."""
        with self.assertRaises(ValueError) as ex:
            factories.CustomUserFactory(email=None)
        message = ex.exception
        self.assertEqual(str(message), "Users must have an email address")

    def test_create_superuser(self):
        """Test for creating superuser."""
        superuser = factories.SuperuserFactory()

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.position, "Owner")

    def test_create_superuser_is_staff_false_error(self):
        """Test for creating superuser with is_staff=False."""
        with self.assertRaises(ValueError) as ex:
            factories.SuperuserFactory(is_staff=False)
        message = ex.exception
        self.assertEqual(str(message), "Superuser must have is_staff=True.")

    def test_create_superuser_is_superuser_false_error(self):
        """Test for creating superuser with is_superuser=False."""
        with self.assertRaises(ValueError) as ex:
            factories.SuperuserFactory(is_superuser=False)
        message = ex.exception
        self.assertEqual(str(message), "Superuser must have is_superuser=True.")

    def test_create_superuser_without_password(self):
        """Test for creating superuser without password, should be error."""
        with self.assertRaises(ValueError) as ex:
            factories.SuperuserFactory(password=None)
        message = ex.exception
        self.assertEqual(str(message), "Superuser must have an password.")

    def test_create_specialist(self):
        """Test for creating specialist."""
        specialist = factories.SpecialistFactory()

        self.assertFalse(specialist.is_staff)
        self.assertFalse(specialist.password)
        self.assertFalse(specialist.is_superuser)
        self.assertTrue(specialist.is_specialist)
        self.assertTrue(specialist.groups.filter(name="Specialist"))

    def test_create_manager(self):
        """Test for creating manager."""
        manager = factories.ManagerFactory()

        self.assertFalse(manager.is_staff)
        self.assertFalse(manager.is_superuser)
        self.assertTrue(manager.is_manager)
        self.assertTrue(manager.groups.filter(name="Manager"))

    def test_create_manager_without_password(self):
        """Test for creating manager without password, should be error."""
        with self.assertRaises(ValueError) as ex:
            factories.ManagerFactory(password=None)
        message = ex.exception
        self.assertEqual(str(message), "Manager must have an password.")

    def test_create_admin(self):
        """Test for creating admin."""
        admin = factories.AdminFactory()

        self.assertFalse(admin.is_staff)
        self.assertFalse(admin.is_superuser)
        self.assertTrue(admin.groups.filter(name="Admin"))
        self.assertTrue(admin.is_admin)

    def test_create_admin_without_password(self):
        """Test for creating admin without password, should be error."""
        with self.assertRaises(ValueError) as ex:
            factories.AdminFactory(password=None)
        message = ex.exception
        self.assertEqual(str(message), "Admin must have an password.")


class CustomUserSerializerTest(TestCase):
    """Class CustomUserSerializerTest for testing CustomUser serializers."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.sp_serializer = SpecialistSerializer
        self.data = factories.SpecialistFactory.build().__dict__

    def tearDown(self):
        """This method deletes all users and cleans avatars' data."""
        CustomUser.objects.all().delete()

    def test_valid_specialist_serializer(self):
        """Check serializer with valid data."""
        serializer = self.sp_serializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        add_user_to_group_specialist(user)
        self.assertEqual(serializer.data["first_name"], self.data["first_name"])
        self.assertEqual(serializer.data["last_name"], self.data["last_name"])
        self.assertEqual(serializer.data["email"], self.data["email"])
        self.assertEqual(serializer.data["position"], self.data["position"])
        self.assertEqual(serializer.data["bio"], self.data["bio"])
        self.assertEqual(serializer.data["patronymic"], self.data["patronymic"])
        self.assertEqual(serializer.data["is_active"], self.data["is_active"])
        self.assertEqual(serializer.data["avatar"], f"/media/images/{self.data['avatar'].name}")
        self.assertIn("Specialist", serializer.data["groups"])
        self.assertIn(factories.GroupFactory(name="Specialist"), user.groups.all())

    def test_empty_serializer(self):
        """Check serializer without data."""
        serializer = self.sp_serializer()
        self.assertEqual(
            serializer.data,
            {
                "email": "",
                "first_name": "",
                "last_name": "",
                "patronymic": "",
                "position": None,
                "bio": "",
                "avatar": None,
                "is_active": True,
            },
        )

    def test_validate_none_data(self):
        """Check serializer with data equal None."""
        serializer = self.sp_serializer(data=None)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {"non_field_errors": ["No data provided"]})


class CustomUserViewTest(APITestCase):
    """Class CustomUserViewTest for testing CustomUser view."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.get_specialists_url_name = "api:specialists-list-create"
        fake_data = factories.SpecialistFactory.build()
        self.specialist_data = {k: getattr(fake_data, k) for k in ["first_name", "last_name", "email", "position"]}

    def tearDown(self):
        """This method deletes all users and cleans avatars' data."""
        CustomUser.objects.all().delete()

    def test_get_all_specialists(self):
        """Test for getting all specialists."""
        factories.SpecialistFactory.create_batch(3)
        response = self.client.get(reverse(self.get_specialists_url_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_specialists_pagination(self):
        """Test specialists pagination."""
        specialists = factories.SpecialistFactory.create_batch(20)
        page_size = 10
        pages = math.ceil(len(specialists) / page_size)
        response = self.client.get(f"{reverse(self.get_specialists_url_name)}?page_size={page_size}&page={pages}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertEqual(response.data["pages"], pages)
        self.assertEqual(response.data["count"], 20)
        self.assertIsNone(response.data["next"])

    def test_specialists_date_schedule_filter(self):
        """Test for filtering specialists by a specific working date."""
        filter_date = fake_data.get_future_datetime(start=1, end=2, force_minute=30).fuzz()
        outside_filter_date = fake_data.get_future_datetime(start=3, end=4, force_minute=30).fuzz()
        end_time = fake_data.get_future_datetime(force_minute=50).fuzz()
        factories.SpecialistScheduleFactory.create_batch(
            10, working_time={filter_date.strftime("%a"): [[time_to_string(filter_date), time_to_string(end_time)]]}
        )
        factories.SpecialistScheduleFactory.create_batch(
            10,
            working_time={
                outside_filter_date.strftime("%a"): [[time_to_string(outside_filter_date), time_to_string(end_time)]]
            },
        )
        response = self.client.get(f"{reverse(self.get_specialists_url_name)}?date={filter_date.strftime('%Y-%m-%d')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.all().count(), 20)
        self.assertEqual(response.data["count"], 10)

    def test_specialists_date_schedule_filter_invalid_data(self):
        """Test for filtering specialists by a specific working date when invalid filter data."""
        response = self.client.get(f"{reverse(self.get_specialists_url_name)}?date=invalid")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])

    def test_specialists_position_filter(self):
        """Test for filtering specialists by position."""
        filter_data = "position_1"
        factories.SpecialistFactory.create_batch(10, position=filter_data)
        factories.SpecialistFactory.create_batch(10, position="position_2")

        response = self.client.get(f"{reverse(self.get_specialists_url_name)}?position={filter_data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.all().count(), 20)
        self.assertEqual(response.data["count"], 10)

    def test_specialists_position_filter_not_exist_position(self):
        """Test for filtering specialists by position when no exist such position."""
        filter_data = "invalid_position"
        factories.SpecialistFactory.create_batch(10, position="position_2")

        response = self.client.get(f"{reverse(self.get_specialists_url_name)}?position={filter_data}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"position": [
            ErrorDetail(string=f"Select a valid choice. {filter_data} is not one of the available choices.",
                        code="invalid_choice")]})

    def test_specialists_position_filter_empty_results(self):
        """Test for filtering specialists by position when no results."""
        filter_data = "position_1"
        factories.SpecialistFactory.create_batch(10, position="position_2")

        response = self.client.get(f"{reverse(self.get_specialists_url_name)}?position={filter_data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])

    def test_create_specialists_by_admin_fail(self):
        """Test for creating specialist by admin."""
        self.client.force_authenticate(factories.AdminFactory())
        response = self.client.post(reverse(self.get_specialists_url_name), self.specialist_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_specialists_by_manager_success(self):
        """Test for creating specialist by manager."""
        self.client.force_authenticate(factories.ManagerFactory())
        response = self.client.post(reverse(self.get_specialists_url_name), self.specialist_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_specialists_by_superuser_success(self):
        """Test for creating specialist by superuser."""
        self.client.force_authenticate(factories.SuperuserFactory())
        response = self.client.post(reverse(self.get_specialists_url_name), self.specialist_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

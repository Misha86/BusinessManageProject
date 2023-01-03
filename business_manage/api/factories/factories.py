"""Module for all factories classes used in the tests."""

import os
from collections import namedtuple
from datetime import timedelta
from random import choice, randint

import factory.fuzzy
from api.models import Appointment, CustomUser, Location, SpecialistSchedule
from api.utils import generate_working_time, generate_working_time_intervals
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils import timezone


class GroupFactory(factory.django.DjangoModelFactory):
    """Factory class for testing Group model."""

    class Meta:
        """Class Meta for the definition of the Group model."""

        model = Group
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: f"Group_{n}")

    @staticmethod
    def groups_for_test():
        """Get all existing groups from the project."""
        groups_name = ["Admin", "Manager", "Specialist"]
        GroupNamed = namedtuple("GroupNamed", groups_name)
        return GroupNamed(*[GroupFactory(name=name) for name in groups_name])


def get_image_path():
    """Get path to the random image in the directory 'api/factories/avatars'."""
    images_dir = settings.BASE_DIR / "api/factories/avatars"
    image = choice(os.listdir(images_dir))
    return os.path.join(images_dir, image)


class CustomUserFactory(factory.django.DjangoModelFactory):
    """Factory class for creating users."""

    class Meta:
        """Class Meta for the definition of the CustomUser model."""

        model = CustomUser

    email = factory.LazyAttributeSequence(
        lambda u, n: f"{u.first_name.lower()}.{u.last_name.lower()}_{n}@example.com")
    first_name = factory.Faker("first_name_male")
    last_name = factory.Faker("last_name_male")
    avatar = factory.django.ImageField(from_path=get_image_path())
    bio = factory.Faker("paragraph", nb_sentences=5)

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        """Add default value for avatar field."""
        if not kwargs["avatar"]:
            kwargs["avatar"] = "default_avatar.jpeg"
        return kwargs

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with custom call create_user."""
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        """Get the field of ManyToMany for groups."""
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)


class SpecialistFactory(CustomUserFactory):
    """Factory class for creating specialists."""

    position = factory.fuzzy.FuzzyChoice(CustomUser.PositionChoices)

    class Params:
        """Extra params for factory.

        If add_schedule=True Schedule is creating for specialist.
        """
        add_schedule = factory.Trait(
            schedule=factory.RelatedFactory(
                "api.factories.factories.SpecialistScheduleFactory", factory_related_name="specialist"
            )
        )

    @factory.post_generation
    def add_to_specialist_group(self, create, extracted, **kwargs):
        """Add user to the group 'Specialist'."""
        if not create:
            return
        group = GroupFactory(name="Specialist")
        self.groups.add(group)


class SuperuserFactory(CustomUserFactory):
    """Factory class for creating superusers."""

    password = factory.LazyAttribute(lambda u: f"0987654321{u.first_name[0]}")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with custom call create_superuser."""
        manager = cls._get_manager(model_class)
        return manager.create_superuser(*args, **kwargs)


class ManagerFactory(SuperuserFactory):
    """Factory class for creating managers."""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with custom call create_manager."""
        manager = cls._get_manager(model_class)
        return manager.create_manager(*args, **kwargs)


class AdminFactory(SuperuserFactory):
    """Factory class for creating admins."""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with custom call create_admin."""
        manager = cls._get_manager(model_class)
        return manager.create_admin(*args, **kwargs)


class LocationFactory(factory.django.DjangoModelFactory):
    """Factory class for creating locations."""

    class Meta:
        """Class Meta for the definition of the Location model."""

        model = Location
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: f"Location_{n}")
    address = factory.Faker("address")

    @factory.lazy_attribute
    def working_time(self):
        """Generates location working time."""
        start_hour = f"{randint(10, 11)}:{choice(range(10, 60, 5))}"
        end_hour = f"{randint(16, 20)}:{choice(range(10, 60, 5))}"

        return generate_working_time(start_hour, end_hour)


class AppointmentFactory(factory.django.DjangoModelFactory):
    """Factory class for creating appointments."""

    class Meta:
        """Class Meta for the definition of the Appointment model."""

        model = Appointment

    duration = timedelta(minutes=20)
    start_time = factory.fuzzy.FuzzyDateTime(
        timezone.localtime(timezone.now()),
        timezone.localtime(timezone.now()) + timedelta(days=10),
        force_hour=13,
        force_minute=30,
        force_second=0,
        force_microsecond=0,
    )
    end_time = factory.LazyAttribute(lambda o: o.start_time + o.duration)
    specialist = factory.SubFactory(SpecialistFactory, add_schedule=True)
    location = factory.SubFactory(LocationFactory)
    customer_email = factory.LazyAttributeSequence(
        lambda c, n: f"{c.customer_firstname.lower()}.{c.customer_lastname.lower()}_{n}@example.com"
    )
    customer_firstname = factory.Faker("first_name_female")
    customer_lastname = factory.Faker("last_name_female")


class SpecialistScheduleFactory(factory.django.DjangoModelFactory):
    """Factory class for creating specialists' schedules."""

    class Meta:
        """Class Meta for the definition of the SpecialistSchedule model."""

        model = SpecialistSchedule
        django_get_or_create = ("specialist",)

    specialist = factory.SubFactory(SpecialistFactory)

    class Params:
        """Extra params for factory.

        working_time_null = False, Working time is becoming None.
        """
        working_time_null = False

    @factory.lazy_attribute
    def working_time(self):
        """Generates location working time."""
        start_hour = f"{randint(10, 11)}:{choice(range(10, 60, 5))}"
        end_hour = f"{randint(16, 20)}:{choice(range(10, 60, 5))}"

        return None if self.working_time_null else generate_working_time_intervals(start_hour, end_hour)

"""Module for all factories classes used in the tests."""

from collections import namedtuple
import factory
from api.models import (CustomUser, Location)
from django.contrib.auth.models import Group
import os
from django.conf import settings
from random import choice, randint
from api.utils import generate_working_time


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
        groups = GroupNamed(*[GroupFactory(name=name) for name in groups_name])
        return groups


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

    email = factory.LazyAttributeSequence(lambda u, n: f"{u.first_name.lower()}.{u.last_name.lower()}_{n}@example.com")
    first_name = factory.Faker("first_name_male")
    last_name = factory.Faker("last_name_male")
    position = factory.fuzzy.FuzzyChoice(CustomUser.PositionChoices)
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
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        """Get the field of ManyToMany for groups."""
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            print(extracted)

            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)


class SuperuserFactory(CustomUserFactory):
    """Factory class for creating superusers."""

    password = factory.LazyAttribute(lambda u: f"0987654321{u.first_name[0]}")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with custom call create_superuser."""
        manager = cls._get_manager(model_class)
        kwargs.update(dict(position=""))
        return manager.create_superuser(*args, **kwargs)


class ManagerFactory(SuperuserFactory):
    """Factory class for creating managers."""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with custom call create_manager."""
        manager = cls._get_manager(model_class)
        kwargs.update(dict(position=""))
        return manager.create_manager(*args, **kwargs)


class AdminFactory(SuperuserFactory):
    """Factory class for creating admins."""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with custom call create_admin."""
        manager = cls._get_manager(model_class)
        kwargs.update(dict(position=""))
        return manager.create_admin(*args, **kwargs)


class LocationFactory(factory.django.DjangoModelFactory):
    """Factory class for creating locations."""

    class Meta:
        """Class Meta for the definition of the Location model."""

        model = Location

    name = factory.Sequence(lambda n: f"Location_{n}")
    address = factory.Faker("address")

    @factory.lazy_attribute
    def working_time(self):
        """Generates location working time."""
        start_hour = f"{randint(6, 9)}:{choice(range(0, 60, 5))}"
        end_hour = f"{randint(13, 20)}:{choice(range(0, 60, 5))}"

        return generate_working_time(start_hour, end_hour)

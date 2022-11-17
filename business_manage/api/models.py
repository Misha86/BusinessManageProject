"""Module for all project models."""
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """This class provides tools for creating and managing CustomUser model."""

    def _create_user(self, email, password=None, group_name=None, **additional_fields):
        """Create and save a user with the given email, and password."""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **additional_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        if group_name:
            user_group, created = Group.objects.get_or_create(name=group_name.title())
            user_group.user_set.add(user)
        return user

    def create_specialist(self, **additional_fields):
        """Creates Specialist.

        Saves user instance with given fields values.
        """
        return self._create_user(group_name="Specialist", **additional_fields)

    def create_admin(self, password, **additional_fields):
        """Creates Admin.

        Saves user instance with given fields values.
        """
        return self._create_user(group_name="Admin", password=password, **additional_fields)

    def create_superuser(self, email: str, password=None, **additional_fields):
        """Creates superuser.

        Saves instance with given fields values
        """
        additional_fields.setdefault("is_staff", True)
        additional_fields.setdefault("is_superuser", True)
        additional_fields.setdefault("position", "Owner")

        if additional_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if additional_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **additional_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """This class represents a custom User model.

    Attributes:
        first_name (str): First name of the user
        last_name (str, optional): Last name of the user
        patronymic (str, optional): Patronymic of the user
        email (str): Email of the user
        updated_at (datetime): Time of the last update
        created_at (datetime): Time when user was created
        bio (str, optional): Additional information about user
        avatar (image, optional): Avatar of the user
    """

    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField("first name", max_length=150)
    last_name = models.CharField("last name", max_length=150)
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    patronymic = models.CharField("patronymic", max_length=150, blank=True)
    position = models.CharField("position", max_length=150)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    bio = models.TextField("bio", max_length=255, blank=True, null=True)
    avatar = models.ImageField(
        "avatar",
        blank=True,
        default="default_avatar.jpeg",
        upload_to="images",
    )

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    REQUIRED_FIELDS = ("first_name", "last_name")

    class Meta:
        """This class meta stores verbose names ordering data."""

        ordering = ["id"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self):
        """str: Returns full name of the user."""
        return self.get_full_name()

    def __repr__(self):
        """str: Returns CustomUser name and its id."""
        return f"{self.__class__.__name__}(id={self.id})"

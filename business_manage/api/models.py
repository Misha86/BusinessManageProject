"""Module for all project models."""
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.db import models
from django.utils import timezone

from api.validators import (validate_rounded_minutes,
                            validate_rounded_minutes_seconds,
                            validate_working_time, validate_specialist, validate_datetime_is_future,
                            validate_working_time_intervals, validate_working_time_values)


def check_password_existing(user_role, password: str):
    """Check if password exists."""
    if not password:
        raise ValueError(f"{user_role} must have an password.")


class UserManager(BaseUserManager):
    """This class provides tools for creating and managing CustomUser model."""

    def create_user(self, email, first_name, last_name, password=None,
                    group_name=None, **additional_fields):
        """Create and save a user with the given email, and password."""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          **additional_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        if group_name:
            user_group, created = Group.objects.get_or_create(name=group_name.title())
            user_group.user_set.add(user)
        return user

    def _create_user_with_role(self, role, password, first_name, last_name, **additional_fields):
        """Creates user with role.

        Saves user instance with given fields values.
        """
        check_password_existing(role, password)
        return self.create_user(group_name=role, password=password,
                                first_name=first_name, last_name=last_name,
                                **additional_fields)

    def create_admin(self, password, first_name, last_name, **additional_fields):
        """Creates Admin.

        Saves user instance with given fields values.
        """
        role = "Admin"
        return self._create_user_with_role(role, password, first_name,
                                           last_name, **additional_fields)

    def create_manager(self, password, first_name, last_name, **additional_fields):
        """Creates Manager.

        Saves user instance with given fields values.
        """
        role = "Manager"
        return self._create_user_with_role(role, password, first_name,
                                           last_name, **additional_fields)

    def create_superuser(self, email, password, first_name, last_name, **additional_fields):
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
        check_password_existing("Superuser", password)

        return self.create_user(email=email, password=password,
                                first_name=first_name, last_name=last_name,
                                **additional_fields)


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
        return f"{self.first_name} {self.last_name}".title()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    @property
    def is_admin(self):
        """Determines whether user is admin."""
        return self.groups.filter(name="Admin").exists()

    @property
    def is_manager(self):
        """Determines whether user is manager."""
        return self.groups.filter(name="Manager").exists()

    def __str__(self):
        """str: Returns full name of the user."""
        return f"{self.get_full_name()} ({self.position})"

    def __repr__(self):
        """str: Returns CustomUser name and its id."""
        return f"{self.__class__.__name__}(id={self.id})"


class Location(models.Model):
    """Class Location provides tools for creating and managing appointments places."""

    name = models.CharField("location name", max_length=200, unique=True)
    address = models.CharField("address", max_length=100, blank=True)
    working_time = models.JSONField(
        "working time",
        default=dict,
        blank=True,
        null=True,
        validators=(validate_working_time,),
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        """This class meta stores verbose names ordering data."""

        ordering = ["id"]
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        """str: Returns name of the location place."""
        return self.name

    def __repr__(self):
        """str: Returns Location name and its id."""
        return f"{self.__class__.__name__}(id={self.id})"


class Appointment(models.Model):
    """This class represents a basic Appointment (for an appointment system).

    Attributes:
        is_active (BooleanField): Status of the appointment
        start_time (datetime): Appointment time and date of it
        end_time (datetime): Time that is calculated according to the duration
        duration (timedelta): The time during which service is provided
        created_at (datetime): Time of creation of the appointment
        specialist (CustomUser): An appointed specialist for the appointment
        customer_firstname (str): Customer first name
        customer_lastname (str): Customer last name
        customer_email (str): Customer email
        note (TextField): Additional note for a specialist
    """

    is_active = models.BooleanField("active", default=True)
    start_time = models.DateTimeField(
        "Start time",
        validators=[validate_rounded_minutes, validate_datetime_is_future],
    )
    end_time = models.DateTimeField(
        "End time",
        blank=True,
        validators=[validate_rounded_minutes, validate_datetime_is_future],
    )
    duration = models.DurationField(
        "duration",
        blank=False,
        validators=[validate_rounded_minutes_seconds],
        help_text="Input only hours and minutes HH:MM:00"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
    )
    specialist = models.ForeignKey(
        CustomUser,
        related_name="specialist_appointments",
        on_delete=models.CASCADE,
        verbose_name="Specialist",
        validators=[validate_specialist]
    )
    customer_firstname = models.CharField("customer firstname", max_length=150)
    customer_lastname = models.CharField("customer lastname", max_length=150)
    customer_email = models.EmailField("customer email", max_length=100)
    location = models.ForeignKey(
        Location,
        related_name="location_appointments",
        on_delete=models.CASCADE,
        verbose_name="Location",
    )
    note = models.TextField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name="Additional note",
    )

    class Meta:
        """This class meta stores verbose names ordering data."""

        ordering = ["id"]
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def save(self, *args, **kwargs):
        """Reimplemented save method for end_time calculation."""
        self.end_time = self.start_time + self.duration
        return super().save(*args, **kwargs)

    def mark_as_completed(self):
        """Marks appointment as completed."""
        self.is_active = False
        self.save(update_fields=["is_active"])

    def __str__(self) -> str:
        """str: Returns a verbose title of the appointment."""
        return f"Appointment #{self.id}"

    def __repr__(self) -> str:
        """str: Returns a string representation of the appointment."""
        return f"Appointment #{self.id}"


class SpecialistSchedule(models.Model):
    """This class represents a specialist schedule (for a schedule system).

    Attributes:
        working_time (JSONField): Specialist working time for a week
        created_at (datetime): Time of creation of the schedule
        update_at (datetime): Time of update of the schedule
        specialist (CustomUser): An appointed specialist for the schedule
    """

    working_time = models.JSONField(
        "working time",
        default=dict,
        blank=True,
        null=True,
        validators=(
            validate_working_time_intervals,
            validate_working_time_values),
    )
    specialist = models.OneToOneField(
        CustomUser,
        related_name="schedule",
        on_delete=models.CASCADE,
        validators=(validate_specialist,),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
    )

    class Meta:
        """This class meta stores verbose names ordering data."""

        ordering = ["id"]
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"

    def __str__(self) -> str:
        """str: Returns a specialist full name with id."""
        return f"Schedule for {self.specialist.get_full_name()} #{self.specialist.id}"

    def __repr__(self) -> str:
        """str: Returns a string representation of the schedule."""
        return f"Schedule #{self.id}"

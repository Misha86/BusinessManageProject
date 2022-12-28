"""The module includes serializers for CustomUser model."""

from api.models import CustomUser
from api.serializers.schedule_serializers import SpecialistScheduleDetailSerializer
from rest_framework import serializers


class GroupListingField(serializers.RelatedField):
    """The custom field for user groups."""

    def to_representation(self, value) -> str:
        """Change representation of instance from id to name.

        Args:
            value (object): instance of group

        Returns:
            object.name (str): attribute-name of an instance
        """
        return value.name

    def to_internal_value(self, data: str) -> int:
        """Reload lookup key from id to name of the instance.

        Args:
            data (str): lookup key (instance name)

        Returns:
            id (int): instance id
        """
        return self.get_queryset().get(name=data).id


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer to retrieve a managers or admins."""

    groups = GroupListingField(many=True, read_only=True)

    class Meta:
        """Class with a model and model fields for serialization."""

        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "avatar",
            "groups",
        ]


class SpecialistSerializer(CustomUserSerializer):
    """Serializer to receive a specific user."""

    is_active = serializers.BooleanField(
        initial=True,
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )

    schedule = SpecialistScheduleDetailSerializer(read_only=True)

    class Meta(CustomUserSerializer.Meta):
        """Class with a model and model fields for serialization."""

        extra_fields = [
            "email",
            "patronymic",
            "position",
            "bio",
            "is_active",
            "schedule",
        ]

        fields = CustomUserSerializer.Meta.fields + extra_fields


class CreateSpecialistSerializer(serializers.ModelSerializer):
    """Serializer to create a specific user."""

    class Meta:
        """Class with a model and model fields for serialization."""

        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "position",
            "bio",
            "avatar",
        ]

"""The module includes serializers for CustomUser model."""

from rest_framework import serializers

from api.models import CustomUser


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


class SpecialistSerializer(serializers.ModelSerializer):
    """Serializer to receive and create a specific user."""

    groups = GroupListingField(many=True, read_only=True)

    class Meta:
        """Class with a model and model fields for serialization."""

        model = CustomUser
        fields = ["email", "first_name", "last_name", "patronymic",
                  "position", "bio", "avatar", "is_active", "groups"]


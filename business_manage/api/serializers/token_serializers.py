"""The module includes serializers for tokens."""

from api.serializers.customuser_serializers import CustomUserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer to add a specific user to the response."""

    def validate(self, attrs):
        """Add user data to the response."""
        data = super().validate(attrs)

        user_serializer = CustomUserSerializer(instance=self.user)

        data["user"] = user_serializer.data

        return data


class RefreshTokenSerializer(serializers.Serializer):
    """Serializer to add token to the black list."""

    refresh = serializers.CharField()

    default_error_messages = {"bad_token": "Token is invalid or expired"}

    def validate(self, attrs):
        """Get refresh token."""
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        """Save refresh token to the black list."""
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")

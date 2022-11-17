"""Services for CustomUser model."""
from django.contrib.auth.models import Group

from api.models import CustomUser


def get_all_specialists():
    return CustomUser.objects.filter(groups__name__icontains="specialist")


def create_specialist(specialist_data):
    return CustomUser.objects.create_specialist(**specialist_data)

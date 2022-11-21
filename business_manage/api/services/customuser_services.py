"""Services for CustomUser model."""

from django.contrib.auth.models import Group

from api.models import CustomUser


def get_all_specialists():
    """Get all specialists."""
    return CustomUser.objects.filter(groups__name__icontains="Specialist")


def add_user_to_group_specialist(user):
    """Create new specialist (CustomUser instance with Group specialist)."""
    user_group, created = Group.objects.get_or_create(name="Specialist")
    user_group.user_set.add(user)

"""Services for CustomUser model."""

from api.models import CustomUser


def get_all_specialists():
    """Get all specialists."""
    return CustomUser.objects.filter(groups__name__icontains="specialist")


def create_specialist(specialist_data):
    """Create new specialist (CustomUser instance with Group specialist)."""
    return CustomUser.objects.create_specialist(**specialist_data)

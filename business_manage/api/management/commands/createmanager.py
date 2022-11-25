"""Management utility to create managers."""

from ._base_command import AbstractCommand


class Command(AbstractCommand):
    """Command to create managers."""

    def __init__(self, *args, **kwargs):
        """Assign values to object properties."""
        super().__init__(*args, **kwargs)
        self.create_user = self.UserModel.objects.create_manager
        self.user_role = "manager"

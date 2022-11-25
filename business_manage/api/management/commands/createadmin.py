"""Management utility to create admins."""

from ._base_command import AbstractCommand


class Command(AbstractCommand):
    """Command to create admins."""

    def __init__(self, *args, **kwargs):
        """Assign values to object properties."""
        super().__init__(*args, **kwargs)
        self.create_user = self.UserModel.objects.create_admin
        self.user_role = "admin"

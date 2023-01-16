"""Management utility to create specialists."""

from django.core.management.base import BaseCommand, CommandError
from api.factories.factories import SpecialistFactory
from api.models import CustomUser
from django.conf import settings


class Command(BaseCommand):
    """Command to create specialists using factories."""

    def add_arguments(self, parser):
        """This method adds named arguments to the command."""
        parser.add_argument("--count", type=int, help="Add count of specialists.", default=0)

        parser.add_argument("--create", help="Create specialists.", action="store_true")

        parser.add_argument("--add_schedule", help="Add schedule to the specialists.", action="store_true")

        parser.add_argument("--delete_all", help="Delete all specialists.", action="store_true")

    def handle(self, *args, **options):
        """This method does all the logic for specialists' DB."""
        if settings.DEBUG:
            if options["create"]:
                specialists_count = options["count"]
                specialists_schedule = options["add_schedule"]
                SpecialistFactory.create_batch(size=specialists_count, add_schedule=specialists_schedule)
                self.stdout.write(self.style.SUCCESS(f"Successfully created {specialists_count} specialists"))
            if options["delete_all"]:
                CustomUser.specialists.all().delete()
                self.stdout.write(self.style.SUCCESS(f"Successfully deleted all specialists"))
        else:
            raise CommandError("Can't execute in production...")

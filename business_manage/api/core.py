"""Module for core functionality."""


from rest_framework.metadata import SimpleMetadata


class CustomMetadata(SimpleMetadata):
    """Include fields information for `OPTIONS` requests."""

    def determine_metadata(self, request, view):
        """Set fields information to the response."""
        if actions := self.determine_actions(request, view):
            return {"fields": actions["POST"]}

"""Module for core functionality."""


from rest_framework.metadata import SimpleMetadata


class CustomMetadata(SimpleMetadata):
    """Include fields information for `OPTIONS` requests."""

    def determine_metadata(self, request, view):
        """Set fields information to the response."""
        if actions := self.determine_actions(request, view):
            data = {}
            for key, value in actions["POST"].items():
                if key == "password":
                    value["type"] = "password"
                elif key == "email":
                    value["type"] = "email"
                elif "image" in value["type"]:
                    value["type"] = "file"
                data[key] = value

            return {"fields": data}

"""Module for pagination classes."""

import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class SpecialistResultsSetPagination(PageNumberPagination):
    """Class for specialists list pagination."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        """Response schema for pagination."""
        return Response(
            {
                "count": self.page.paginator.count,
                "pages": self.get_pages_count(),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )

    def get_pages_count(self):
        """Get count of pages."""
        if data_count := self.page.paginator.count:
            page_size = self.get_page_size(self.request)
            return math.ceil(data_count / page_size)

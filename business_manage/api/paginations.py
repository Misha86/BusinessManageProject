"""Module for pagination classes."""

from rest_framework.pagination import PageNumberPagination


class SpecialistResultsSetPagination(PageNumberPagination):
    """Class for specialists list pagination."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 1000

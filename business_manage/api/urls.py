"""Api URL Configuration."""

import pytz
from django.urls import path, register_converter
from django.utils.timezone import datetime
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "api"


class DateConverter:
    """Converter class for passing date in urls.

    Provide to_python and to_url methods.
    """

    regex = r"\d{4}-\d{1,2}-\d{1,2}"

    def to_python(self, value):
        """Converts date from url to python datetime object."""
        return pytz.utc.localize(datetime.strptime(value, "%Y-%m-%d"))

    def to_url(self, value):
        """Return date value from url."""
        return value


register_converter(DateConverter, "date")

urlpatterns = [
    path("specialists/", views.SpecialistList.as_view(), name="specialists-list-create"),
    path("specialists/<int:pk>/", views.SpecialistDetail.as_view(), name="Specialist-detail"),
    path("locations/", views.LocationList.as_view(), name="locations-list-create"),
    path("appointments/", views.AppointmentList.as_view(), name="appointments-list-create"),
    path("appointments/<int:pk>/", views.AppointmentDetail.as_view(), name="appointment-detail"),
    path("schedules/", views.SpecialistScheduleList.as_view(), name="schedules-list-create"),
    path("specialists/<int:pk>/schedule/", views.SpecialistScheduleDetail.as_view(), name="specialist-schedule"),
    path(
        "specialists/<int:s_id>/schedule/<date:a_date>/",
        views.SpecialistDateScheduleView.as_view(),
        name="specialist-schedule-date",
    ),
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/logout/", views.LogoutView.as_view(), name="token_logout"),
]

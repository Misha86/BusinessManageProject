"""Api URL Configuration."""

from django.urls import path
from . import views


app_name = "api"


urlpatterns = [
    path("specialists/", views.SpecialistList.as_view(), name="specialists-list-create"),
    path("locations/", views.LocationList.as_view(), name="locations-list-create"),
    path("appointments/", views.AppointmentList.as_view(), name="appointments-list-create"),
]

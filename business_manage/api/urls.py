"""Api URL Configuration."""

from django.urls import path
from . import views


app_name = "api"


urlpatterns = [
    path("specialists/", views.SpecialistList.as_view(), name="specialists-list-create"),
    path("specialists/<int:pk>/", views.SpecialistDetail.as_view(), name="Specialist-detail"),
    path("locations/", views.LocationList.as_view(), name="locations-list-create"),
    path("appointments/", views.AppointmentList.as_view(), name="appointments-list-create"),
    path("appointments/<int:pk>/", views.AppointmentDetail.as_view(), name="appointment-detail"),
    path("schedules/", views.SpecialistScheduleList.as_view(), name="schedules-list-create"),
    path("specialists/<int:pk>/schedule/",
         views.SpecialistScheduleDetail.as_view(),
         name="specialist-schedule"),
]

"""Api URL Configuration."""

from django.urls import path
from . import views


app_name = "api"


urlpatterns = [
    path("specialists/", views.SpecialistList.as_view(), name="specialists-list-create"),
]

"""All Api URLs."""

from django.urls import path
from . import views


app_name = "api"


urlpatterns = [
    path('specialists/', views.SpecialistList.as_view(), name="specialist-list-create"),
]


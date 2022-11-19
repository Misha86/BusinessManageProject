"""Business_manage projects views."""

from rest_framework import generics, status
from rest_framework.response import Response

from .models import Appointment
from .serializers.appointment_serializers import AppointmentSerializer
from .serializers.customuser_serializers import SpecialistSerializer
from api.services import custom_user_services as us
from .permissions import ReadOnly, IsBusinessOwnerOrManager, IsBusinessOwnerOrAdmin
from .serializers.location_serializers import LocationSerializer
from .services.location_services import get_locations_with_working_days


class SpecialistList(generics.ListCreateAPIView):
    """SpecialistList class for creating and reviewing specialists."""

    queryset = us.get_all_specialists()
    serializer_class = SpecialistSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrManager]

    def post(self, request, *args, **kwargs):
        """Post method for creating specialists."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        specialist = self.get_serializer(us.create_specialist(serializer.validated_data))
        headers = self.get_success_headers(specialist.data)
        return Response(specialist.data, status=status.HTTP_201_CREATED, headers=headers)


class LocationList(generics.ListCreateAPIView):
    """LocationList class for creating and reviewing locations."""

    queryset = get_locations_with_working_days()
    serializer_class = LocationSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrManager]


class AppointmentList(generics.ListCreateAPIView):
    """AppointmentList class for creating and reviewing appointments."""

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrAdmin]

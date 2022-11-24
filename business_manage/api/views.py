"""Business_manage projects views."""

from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Appointment, SpecialistSchedule, CustomUser
from .serializers.appointment_serializers import AppointmentSerializer
from .serializers.customuser_serializers import SpecialistSerializer
from .serializers.schedule_serializers import (SpecialistScheduleSerializer,
                                               SpecialistScheduleDetailSerializer)
from .services import customuser_services as us
from .permissions import ReadOnly, IsBusinessOwnerOrManager, IsBusinessOwnerOrAdmin
from .serializers.location_serializers import LocationSerializer
from .services import location_services as ls


class SpecialistList(generics.ListCreateAPIView):
    """SpecialistList class for creating and reviewing specialists."""

    queryset = us.get_all_specialists()
    serializer_class = SpecialistSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrManager]
    filterset_fields = ["position"]

    def post(self, request, *args, **kwargs):
        """Post method for creating specialists."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        us.add_user_to_group_specialist(serializer.save())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SpecialistDetail(generics.RetrieveUpdateDestroyAPIView):
    """SpecialistDetail class for updating and reviewing specialist."""

    queryset = us.get_all_specialists()
    serializer_class = SpecialistSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrManager]


class LocationList(generics.ListCreateAPIView):
    """LocationList class for creating and reviewing locations."""

    queryset = ls.get_all_locations()
    serializer_class = LocationSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrManager]


class AppointmentList(generics.ListCreateAPIView):
    """AppointmentList class for creating and reviewing appointments."""

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrAdmin]


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """AppointmentList class for updating and reviewing appointment detail."""

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrAdmin]


class SpecialistScheduleList(generics.ListCreateAPIView):
    """SpecialistScheduleList class for creating and reviewing schedules."""

    queryset = SpecialistSchedule.objects.all()
    serializer_class = SpecialistScheduleSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrManager]


class SpecialistScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    """SpecialistScheduleDetail class for updating and reviewing specialist schedules."""

    serializer_class = SpecialistScheduleDetailSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrManager]

    def get_object(self):
        """Get schedule for specific specialist."""
        specialist_id = self.kwargs["pk"]
        specialist = get_object_or_404(CustomUser,
                                       id=specialist_id,
                                       groups__name__icontains="Specialist")
        return specialist.schedule

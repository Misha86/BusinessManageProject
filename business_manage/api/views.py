"""Business_manage projects views."""

from rest_framework import generics, status
from rest_framework.response import Response

from .models import Appointment, SpecialistSchedule
from .serializers.appointment_serializers import AppointmentSerializer
from .serializers.customuser_serializers import SpecialistSerializer
from .serializers.schedule_serializers import SpecialistScheduleSerializer
from .services import customuser_services as us
from .permissions import ReadOnly, IsBusinessOwnerOrManager, IsBusinessOwnerOrAdmin
from .serializers.location_serializers import LocationSerializer
from .services import location_services as ls


class SpecialistList(generics.ListCreateAPIView):
    """SpecialistList class for creating and reviewing specialists."""

    queryset = us.get_all_specialists()
    serializer_class = SpecialistSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrManager]

    def post(self, request, *args, **kwargs):
        """Post method for creating specialists."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        us.add_user_to_group_specialist(serializer.save())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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

    # def post(self, request, *args, **kwargs):
    #     """Post method for creating specialists."""
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     a_data = serializer.validated_data
    #
    #     start_time = a_data.get("start_time")
    #     end_time = start_time + a_data.get("duration")
    #     location = a_data.get("location")
    #     specialist = a_data.get("specialist")
    #
    #     validate_free_time_interval((start_time, end_time), specialist, location)
    #
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SpecialistScheduleList(generics.ListCreateAPIView):
    """SpecialistScheduleList class for creating and reviewing schedules."""

    queryset = SpecialistSchedule.objects.all()
    serializer_class = SpecialistScheduleSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrManager]

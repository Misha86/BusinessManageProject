"""Business_manage projects views."""

from django.contrib.auth import logout
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .filters import SpecialistFilter
from .models import Appointment, CustomUser, SpecialistSchedule
from .permissions import IsBusinessOwnerOrAdmin, IsBusinessOwnerOrManager, ReadOnly
from .serializers.appointment_serializers import AppointmentSerializer
from .serializers.customuser_serializers import (
    CreateSpecialistSerializer,
    SpecialistSerializer,
)
from .serializers.location_serializers import LocationSerializer
from .serializers.schedule_serializers import (
    SpecialistScheduleDetailSerializer,
    SpecialistScheduleSerializer,
)
from .serializers.token_serializers import (
    MyTokenObtainPairSerializer,
    RefreshTokenSerializer,
)
from .services import customuser_services as us
from .services import location_services as ls
from .services.appointment_services import get_appointments_time_intervals
from .services.schedule_services import get_free_time_intervals, get_working_day


class SpecialistList(generics.ListCreateAPIView):
    """SpecialistList class for creating and reviewing specialists."""

    queryset = us.get_all_specialists().order_by("email")
    serializer_class = CreateSpecialistSerializer
    permission_classes = [ReadOnly | IsBusinessOwnerOrManager]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = SpecialistFilter
    ordering_fields = ["email", "position", "first_name"]

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
        specialist = get_object_or_404(
            CustomUser,
            id=specialist_id,
            groups__name__icontains="Specialist",
        )
        return specialist.schedule


class SpecialistDateScheduleView(APIView):
    """View for displaying specialist's schedule for concrete day."""

    def get(self, request, s_id, a_date):
        """GET method for retrieving schedule."""
        specialist = get_object_or_404(CustomUser, id=s_id)
        name = specialist.get_full_name()
        if not specialist.is_specialist:
            return Response(
                {"detail": f"User {name} is not specialist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if a_date.date() < timezone.now().date():
            return Response(
                {"detail": "You can't see schedule of the past days."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        working_time = specialist.schedule.working_time
        schedule_intervals = get_working_day(working_time, a_date)

        if not any(schedule_intervals):
            return Response(
                {"detail": f"{name} is not working on this day"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        a_intervals = get_appointments_time_intervals(specialist, a_date)

        free_time_intervals = get_free_time_intervals(schedule_intervals, a_intervals)

        all_intervals = {
            "appointments intervals": a_intervals,
            "free intervals": free_time_intervals,
        }
        return Response(
            all_intervals,
            status=status.HTTP_200_OK,
        )


class MyTokenObtainPairView(TokenObtainPairView):
    """MyTokenObtainPairView class for creating and retrieving user tokens."""

    serializer_class = MyTokenObtainPairSerializer


class LogoutView(generics.GenericAPIView):
    """LogoutView class for logging out."""

    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args):
        """Method to logout the user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

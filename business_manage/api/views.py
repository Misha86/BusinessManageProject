from rest_framework import generics, status
from rest_framework.response import Response

from .serializers.customuser_serializers import SpecialistSerializer
from api.services import custom_user_services as us


class SpecialistList(generics.ListCreateAPIView):
    queryset = us.get_all_specialists()
    serializer_class = SpecialistSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        specialist = self.get_serializer(us.create_specialist(serializer.validated_data))
        headers = self.get_success_headers(specialist.data)
        return Response(specialist.data, status=status.HTTP_201_CREATED, headers=headers)





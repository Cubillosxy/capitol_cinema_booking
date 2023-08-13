from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from screenings.api.serializers import ScreeningSerializer
from screenings.services.screening_service import ScreeningService


class ScreeningCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ScreeningSerializer(data=request.data)
        if serializer.is_valid():
            screening = ScreeningService.create_screening(serializer.validated_data)
            serialized_screening = ScreeningSerializer(screening).data
            return Response(serialized_screening, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScreeningAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, screening_id):
        screening = ScreeningService.get_screening_by_id(screening_id)
        if screening is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serialized_screening = ScreeningSerializer(screening).data
        return Response(serialized_screening)

    def put(self, request, screening_id):
        screening = ScreeningService.get_screening_by_id(screening_id)
        if screening is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ScreeningSerializer(screening, data=request.data)
        if serializer.is_valid():
            updated_screening = ScreeningService.update_screening(
                screening, serializer.validated_data
            )
            serialized_screening = ScreeningSerializer(updated_screening).data
            return Response(serialized_screening)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, screening_id):
        screening = ScreeningService.get_screening_by_id(screening_id)
        if screening is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ScreeningService.disable_screening(screening)
        return Response(status=status.HTTP_204_NO_CONTENT)

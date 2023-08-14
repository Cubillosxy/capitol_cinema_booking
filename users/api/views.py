from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import UserLoginSerializer
from users.services.user_services import UserService


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            if UserService.authenticate(request, request.data):
                return Response(
                    {"detail": "Logged in successfully!"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            if UserService.register_user(request, request.data):
                return Response(
                    {"detail": "Registered successfully!"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def get(self, request):
        if UserService.logout_user(request):
            return Response(
                {"detail": "Logged out successfully!"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

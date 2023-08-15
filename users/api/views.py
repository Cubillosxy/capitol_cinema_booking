from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import UserLoginSerializer, UserSerializer
from users.services.mixings import PermissionMixin
from users.services.user_services import UserService


class UserDetailView(PermissionMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):  # pylint: disable=unused-argument
        user_data = UserService.get_user_data(pk)
        serializer = UserSerializer(user_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="set_owner_permissions")
    def set_owner_permissions(self, request, pk=None):
        UserService.set_owner_permissions(pk)
        return Response(status=status.HTTP_200_OK)


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

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import Group

from users.dataclasses import UserData
from utils.instance_utils import get_data_instance
from utils.security import add_salt_to_password

User = get_user_model()


class UserDatabaseService:
    @classmethod
    def _get_user_by_id(cls, user_id: int) -> User:
        return User.objects.get(id=user_id)

    @classmethod
    def _user_has_permission(cls, user_id: int, permission: str) -> bool:
        user = cls._get_user_by_id(user_id)
        return user.has_perm(permission)

    @classmethod
    def _user_has_booking_view_permission(cls, user_id: int) -> bool:
        return cls._user_has_permission(user_id, "users.can_view_bookings")

    @classmethod
    def _user_exists(cls, username) -> bool:
        return User.objects.filter(username=username).exists()

    @classmethod
    def _create_user(cls, username, password) -> User:
        return User.objects.create_user(username=username, password=password)

    @classmethod
    def _add_group_permision(cls, user: User, group_name) -> None:
        group = Group.objects.get(name=group_name)
        user.groups.add(group)


class UserService(UserDatabaseService):
    @classmethod
    def set_owner_permissions(cls, user_id: int) -> bool:
        user = cls._get_user_by_id(user_id)
        cls._add_group_permision(user, group_name="Cinema Owner")
        return True

    @classmethod
    def get_user_data(cls, user_id: int) -> dict:
        user = cls._get_user_by_id(user_id)
        return get_data_instance(UserData, user)

    @classmethod
    def authenticate(cls, request, data) -> bool:
        username = data.get("username")
        password = add_salt_to_password(data.get("password"))
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        return False

    @classmethod
    def register_user(cls, request, data) -> bool:
        username = data.get("username")
        password = add_salt_to_password(data.get("password"))
        if cls._user_exists(username):
            return False
        user = cls._create_user(username, password)
        login(request, user)
        return True

    @classmethod
    def logout_user(cls, request) -> bool:
        logout(request)
        return True

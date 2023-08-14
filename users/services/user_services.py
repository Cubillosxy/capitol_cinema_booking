from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model()

from utils.security import add_salt_to_password


class UserDatabaseService:
    @classmethod
    def _get_user_by_id(cls, user_id: int) -> User:
        return User.objects.get(id=user_id)

    @classmethod
    def _user_has_permission(cls, user_id: int, permission: str) -> bool:
        user = cls._get_user_by_id(user_id)
        return user.has_perm(permission)

    @classmethod
    def _user_exists(cls, username) -> bool:
        return User.objects.filter(username=username).exists()

    @classmethod
    def _create_user(cls, username, password) -> User:
        return User.objects.create_user(username=username, password=password)


class UserService:
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
        if UserDatabaseService._user_exists(username):
            return False
        user = UserDatabaseService._create_user(username, password)
        login(request, user)
        return True

    @classmethod
    def logout_user(cls, request) -> bool:
        logout(request)
        return True

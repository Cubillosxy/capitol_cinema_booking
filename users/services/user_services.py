from django.contrib.auth import get_user_model

User = get_user_model()


class UserDatabaseService:
    @classmethod
    def _get_user_by_id(cls, user_id: int) -> User:
        return User.objects.get(id=user_id)

    @classmethod
    def _user_has_permission(cls, user_id: int, permission: str) -> bool:
        user = cls._get_user_by_id(user_id)
        return user.has_perm(permission)

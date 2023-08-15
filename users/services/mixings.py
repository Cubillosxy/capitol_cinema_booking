from users.services.user_services import UserDatabaseService


class PermissionMixin:
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if (
            not UserDatabaseService._user_has_booking_view_permission(request.user.id)
            and not request.user.is_staff
        ):
            self.permission_denied(
                request, message="You do not have permission to view this user"
            )

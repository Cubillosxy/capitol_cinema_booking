from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Movie API",
        default_version="v1",
        description="Booking system for movie tickets",
        license=openapi.License(name="GNU GENERAL PUBLIC LICENSE"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

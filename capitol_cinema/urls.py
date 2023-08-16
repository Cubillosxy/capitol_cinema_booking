"""
URL configuration for capitol_cinema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from utils.docs import schema_view

urlpatterns = [
    path("s3cr3t-adm1n/", admin.site.urls),
    path("cinemas/", include("cinemas.api.urls", namespace="cinemas")),
    path("movies/", include("movies.api.urls", namespace="movies")),
    path("screenings/", include("screenings.api.urls", namespace="screenings")),
    path("bookings/", include("bookings.api.urls", namespace="bookings")),
    path("users/", include("users.api.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "api-doc/",
            schema_view.with_ui("swagger", cache_timeout=10),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=10),
            name="schema-redoc",
        ),
    ]

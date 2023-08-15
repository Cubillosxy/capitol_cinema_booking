from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.api import views

router = DefaultRouter()

router.register(r"detail", views.UserDetailView, basename="detail")


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="user-register"),
    path("login/", views.LoginView.as_view(), name="user-login"),
    path("logout/", views.LogoutView.as_view(), name="user-logout"),
    path("", include(router.urls)),
]

app_name = "users"

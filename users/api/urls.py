from django.urls import path

from users.api import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="user-register"),
    path("login/", views.LoginView.as_view(), name="user-login"),
    path("logout/", views.LogoutView.as_view(), name="user-logout"),
]

app_name = "users"

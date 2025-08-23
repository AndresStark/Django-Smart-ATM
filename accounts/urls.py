from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import RegisterUserView, AccountCreationView, AccountDashboardView

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="users/login.html"),
        name="login"
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="users/logout.html"),
        name="logout"
    ),
    path(
        "register/",
        RegisterUserView.as_view(template_name="users/register.html"),
        name="register"
    ),
    path("create/", AccountCreationView.as_view(), name="create"),
    path("dashboard/", AccountDashboardView.as_view(), name="dashboard"),
]
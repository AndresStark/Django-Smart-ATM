from django.urls import path

from .views import HomeView

app_name = "atm"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # path("transaction/", views.IndexView.as_view(), name="atm"),
]
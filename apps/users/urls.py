from django.urls import path

from apps.users.views import RegisterView

app_name = "users"

urlpatterns = [
    path("", RegisterView.as_view(), name="register"),
]

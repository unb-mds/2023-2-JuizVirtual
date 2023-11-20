from django.urls import path
from django.views.generic import TemplateView

from apps.users.views import RegisterView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "",
        TemplateView.as_view(template_name="users/profile.html"),
        name="profile",
    ),
]

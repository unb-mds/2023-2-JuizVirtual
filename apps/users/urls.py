from django.urls import path

from apps.users.views import ProfileView, RegisterView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "profile/<str:user_username>/", ProfileView.as_view(), name="profile"
    ),
]

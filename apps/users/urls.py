from django.urls import path

from apps.users.views import ProfileView, RankingView, RegisterView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<str:username>/", ProfileView.as_view(), name="profile"),
    path("ranking/", RankingView.as_view(), name="ranking"),
]

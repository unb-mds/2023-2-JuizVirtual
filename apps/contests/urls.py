from django.urls import path

from apps.contests.views import DetailView, IndexView, send

app_name = "contests"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:pk>/", DetailView.as_view(), name="detail"),
    path("<int:contest_id>/send/", send, name="send"),
]

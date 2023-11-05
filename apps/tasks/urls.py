from django.urls import path

from apps.tasks.views import DetailView

app_name = "tasks"

urlpatterns = [
    path("<int:pk>/", DetailView.as_view(), name="detail"),
]

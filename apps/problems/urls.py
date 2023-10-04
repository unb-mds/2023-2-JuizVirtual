from django.urls import path

from apps.problems.views import DetailView

app_name = "problems"

urlpatterns = [
    path("<int:pk>/", DetailView.as_view(), name="detail"),
]

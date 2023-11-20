from django.urls import path
from django.views.generic import TemplateView

app_name = "submissions"

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="submissions/submit.html"),
        name="submissions",
    )
]

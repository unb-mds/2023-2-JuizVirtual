from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

home_view = TemplateView.as_view(template_name="pages/home.html")
register_view = TemplateView.as_view(
    template_name="registration/register.html"
)

urlpatterns = [
    # Django views
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    # Local views
    path("", home_view, name="home"),
    path("contests/", include("apps.contests.urls")),
]

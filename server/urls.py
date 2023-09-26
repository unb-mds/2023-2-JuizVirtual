from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

home_view = TemplateView.as_view(template_name="pages/home.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("", home_view, name="home"),
]

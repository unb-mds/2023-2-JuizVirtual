from django.contrib import admin
from django.urls import include, path

from apps.contests.views import IndexView

urlpatterns = [
    # Django views
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    # Local views
    path("", IndexView.as_view(), name="home"),
    path("contests/", include("apps.contests.urls")),
    path("problems/", include("apps.problems.urls")),
    path("register/", include("apps.users.urls")),
]

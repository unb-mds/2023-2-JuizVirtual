from django.contrib import admin
from django.urls import include, path

from apps.contests.views import IndexView

urlpatterns = [
    # Django views
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    # Local views
    path("", IndexView.as_view(), name="home"),
    path("contests/", include("apps.contests.urls"), name="contests"),
    path("tasks/", include("apps.tasks.urls")),
    path("", include("apps.users.urls")),
    path("submissions/", include("apps.submissions.urls")),
]

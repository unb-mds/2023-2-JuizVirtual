from django.urls import path

from apps.submissions.views import SubmissionListView

app_name = "submissions"

urlpatterns = [path("", SubmissionListView.as_view(), name="list")]

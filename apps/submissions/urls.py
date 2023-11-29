from django.urls import path

from apps.submissions.views import SubmissionListView

urlpatterns = [
    path("submissions/", SubmissionListView.as_view(), name="submission_list")
]

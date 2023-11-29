from django.views.generic import ListView

from apps.submissions.models import Submission


class SubmissionListView(ListView[Submission]):
    model = Submission
    template_name = "submission_list.html"
    context_object_name = "submissions"

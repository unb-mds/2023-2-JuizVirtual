from typing import TYPE_CHECKING

from django.views.generic import ListView

from apps.submissions.models import Submission

if TYPE_CHECKING:
    SubmissionViewBase = ListView[Submission]
else:
    SubmissionViewBase = ListView


class SubmissionListView(SubmissionViewBase):
    model = Submission
    template_name = "submissions/list.html"
    context_object_name = "submissions"

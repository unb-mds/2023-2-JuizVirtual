from typing import TYPE_CHECKING

from django.db.models import QuerySet
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
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Submission]:
        return Submission._default_manager.all().order_by("-created_at")

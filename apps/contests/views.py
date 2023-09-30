import sys
from io import StringIO
from typing import TYPE_CHECKING

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic

from apps.contests.models import Contest

if TYPE_CHECKING:
    IndexViewBase = generic.ListView[Contest]
    DetailViewBase = generic.DetailView[Contest]
else:
    IndexViewBase = generic.ListView
    DetailViewBase = generic.DetailView


class IndexView(IndexViewBase):
    template_name = "contests/index.html"
    context_object_name = "contests"

    def get_queryset(self) -> QuerySet[Contest]:
        return Contest._default_manager.order_by("-start_time")[:5]


class DetailView(DetailViewBase):
    model = Contest
    template_name = "contests/detail.html"


def send(request: HttpRequest, contest_id: int) -> HttpResponse:
    contest = get_object_or_404(Contest, pk=contest_id)
    code = request.POST["code"]

    old_stdout = sys.stdout
    sys.stdout = buffer = StringIO()

    try:
        eval(code)
    except Exception as exc:
        sys.stdout = old_stdout
        return HttpResponse(f"Contest {contest.title} failed.\n{exc}")

    sys.stdout = old_stdout
    message = buffer.getvalue()

    return HttpResponse(
        f"Contest {contest.title} ran successfully.\n{message}"
    )

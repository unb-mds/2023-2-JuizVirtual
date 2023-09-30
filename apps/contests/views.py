from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic

from apps.contests.models import Contest


class IndexView(generic.ListView[Contest]):
    template_name = "contests/index.html"
    context_object_name = "contests"

    def get_queryset(self) -> QuerySet[Contest]:
        return Contest._default_manager.order_by("-start_time")[:5]


class DetailView(generic.DetailView[Contest]):
    model = Contest
    template_name = "contests/detail.html"


def send(request: HttpRequest, contest_id: int) -> HttpResponse:
    contest = get_object_or_404(Contest, pk=contest_id)
    code = request.POST["code"]

    eval(code)

    return HttpResponse(f"Contest {contest.title} ran successfully.")

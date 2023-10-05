from typing import TYPE_CHECKING, Any

from django.db.models.query import QuerySet
from django.views import generic

from apps.contests.enums import ContestStatus
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
        return Contest._default_manager.order_by("start_time")[:5]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["valid_statuses"] = (ContestStatus.PENDING, ContestStatus.RUNNING)

        return ctx


class DetailView(DetailViewBase):
    model = Contest
    template_name = "contests/detail.html"

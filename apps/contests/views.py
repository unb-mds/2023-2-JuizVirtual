from typing import TYPE_CHECKING

from django.db.models.query import QuerySet
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
        return Contest._default_manager.order_by("start_time")[:5]


class DetailView(DetailViewBase):
    model = Contest
    template_name = "contests/detail.html"

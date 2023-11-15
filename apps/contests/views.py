from typing import TYPE_CHECKING, Any

from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.utils import timezone
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
        queryset = Contest._default_manager.filter(
            start_time__gte=timezone.now()
        ).order_by("start_time")[:5]
        if not queryset.exists():
            raise ValidationError("Não há concursos futuros disponíveis.")
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["valid_statuses"] = (ContestStatus.PENDING, ContestStatus.RUNNING)

        return ctx


class DetailView(DetailViewBase):
    model = Contest
    template_name = "contests/detail.html"

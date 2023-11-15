from typing import TYPE_CHECKING, Any, Dict

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
        return Contest._default_manager.order_by("-start_time")[:5]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        # Serve para separar os concursos que estão com status pendente
        # ou em andamento dos concursos que já aconteceram ou que foram
        # cancelados. Precisamos separar para que o template possa
        # exibir os contests de forma diferente.
        ctx["valid_statuses"] = (ContestStatus.PENDING, ContestStatus.RUNNING)
        return ctx


class DetailView(DetailViewBase):
    model = Contest
    template_name = "contests/detail.html"

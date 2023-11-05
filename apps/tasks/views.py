from typing import TYPE_CHECKING

from django.views import generic

from apps.tasks.models import Task

if TYPE_CHECKING:
    DetailViewBase = generic.DetailView[Task]
else:
    DetailViewBase = generic.DetailView


class DetailView(DetailViewBase):
    model = Task
    template_name = "tasks/detail.html"

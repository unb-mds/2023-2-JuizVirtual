from typing import TYPE_CHECKING, Any, Dict

from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.views.generic.edit import FormMixin

from apps.tasks.forms import TaskForm
from apps.tasks.models import Task

if TYPE_CHECKING:
    DetailViewBase = generic.DetailView[Task]
    FormMixinBase = FormMixin[TaskForm]
else:
    DetailViewBase = generic.DetailView
    FormMixinBase = FormMixin


class DetailView(FormMixinBase, DetailViewBase):
    model = Task
    template_name = "tasks/detail.html"
    form_class = TaskForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = TaskForm()

        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        self.object = self.get_object()
        form = self.get_form()

        return (
            self.form_valid(form)
            if form.is_valid()
            else self.form_invalid(form)
        )

    def form_valid(self, form: TaskForm) -> HttpResponse:
        return super().form_valid(form)

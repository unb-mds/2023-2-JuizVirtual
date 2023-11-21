from typing import TYPE_CHECKING, Any, Dict

from djago.db.models import TextField
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views import View, generic
from django.views.generic.edit import FormMixin

from apps.submissions.models import Submission
from apps.tasks.forms import TaskForm
from apps.tasks.models import Task

if TYPE_CHECKING:
    DetailViewBase = generic.DetailView[Task]
    FormMixinBase = FormMixin[TaskForm]
else:
    DetailViewBase = generic.DetailView
    FormMixinBase = FormMixin


class DetailView(FormMixinBase, DetailViewBase, View):
    model = Task
    template_name = "tasks/detail.html"
    form_class = TaskForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = TaskForm()

        return context

    def get_success_url(self) -> str:
        return reverse("tasks:detail", args=[self.object.id])

    def post(self, request: HttpRequest, *, pk: int) -> HttpResponse:
        self.object = self.get_object()
        form = self.get_form()

        if self.form_valid(form):
            submission = Submission()

            submission.code = TextField(request.POST)
            submission.author = request.user
            submission.task = self.object

            submission.save()

        return (
            self.form_valid(form)
            if form.is_valid()
            else self.form_invalid(form)
        )

    def form_valid(self, form: TaskForm) -> HttpResponse:
        return super().form_valid(form)

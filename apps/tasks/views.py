from typing import TYPE_CHECKING, Any, Dict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from apps.submissions.forms import SubmissionForm
from apps.submissions.models import Submission
from apps.tasks.models import Task

if TYPE_CHECKING:
    DetailViewBase = generic.DetailView[Task]
    FormMixinBase = FormMixin[SubmissionForm]
else:
    DetailViewBase = generic.DetailView
    FormMixinBase = FormMixin


class DetailView(FormMixinBase, DetailViewBase):
    model = Task
    template_name = "tasks/detail.html"
    form_class = SubmissionForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = SubmissionForm()

        return context

    def get_success_url(self) -> str:
        return reverse("tasks:detail", args=[self.object.id])

    def post(self, request: HttpRequest, *, pk: int) -> HttpResponse:
        # Unauthenticated users should not be able to submit
        # a submission to a task, so we redirect them to the
        # login page.
        if not request.user.is_authenticated:
            return redirect("login")

        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            Submission._default_manager.create(
                code=request.POST, task=self.object, author=request.user
            )

        return (
            self.form_valid(form)
            if form.is_valid()
            else self.form_invalid(form)
        )

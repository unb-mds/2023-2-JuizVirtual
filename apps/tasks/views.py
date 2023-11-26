import sys
from io import StringIO
from traceback import format_exc
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


def handle_submission(request: HttpRequest, task: Task) -> HttpResponse:
    submission = Submission._default_manager.create(
        code=request.POST["code"],
        task=task,
        author=request.user,
    )

    input_data = StringIO(task.input_file)

    old_stdin = sys.stdin
    sys.stdin = input_data

    old_stdout = sys.stdout
    sys.stdout = stdout = StringIO()

    try:
        eval(compile(request.POST["code"], "<string>", "exec"))
    except Exception as exc:
        submission.status = "RE"
        submission.save()

        return HttpResponse(f"Error: {exc} {format_exc()}")
    finally:
        sys.stdout = old_stdout
        sys.stdin = old_stdin

    output = stdout.getvalue()

    if output == task.output_file:
        submission.status = "AC"
        submission.save()
        return HttpResponse("Correct!")
    else:
        submission.status = "WA"
        submission.save()
        return HttpResponse("Incorrect!")


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

        if not form.is_valid():
            return self.form_invalid(form)

        return handle_submission(request, self.object)

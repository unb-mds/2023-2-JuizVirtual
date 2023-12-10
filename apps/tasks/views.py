import os
import sys
from io import StringIO
from typing import TYPE_CHECKING, Any, Dict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from apps.submissions.forms import SubmissionForm, UploadFileForm
from apps.submissions.models import Submission, SubmissionStatus
from apps.tasks.models import Task
from server import celery

if TYPE_CHECKING:
    DetailViewBase = generic.DetailView[Task]
    FormMixinBase = FormMixin[SubmissionForm]
else:
    DetailViewBase = generic.DetailView
    FormMixinBase = FormMixin


@celery.task(ignore_result=True)
def handle_submission(code: str, task_id: int, submission_id: int) -> None:
    task = Task._default_manager.get(id=task_id)
    submission = Submission._default_manager.get(id=submission_id)

    input_data = StringIO(task.input_file)

    old_stdin = sys.stdin
    sys.stdin = input_data

    old_stdout = sys.stdout
    sys.stdout = stdout = StringIO()

    try:
        eval(compile(code, "<string>", "exec"))
    except Exception:
        submission.status = "RE"
        submission.save()
        return
    finally:
        sys.stdout = old_stdout
        sys.stdin = old_stdin

    output = stdout.getvalue()

    submission.status = "AC" if output == task.output_file else "WA"
    submission.save()

    has_already_scored = (
        Submission._default_manager.filter(
            author=submission.author,
            task=task,
            status=SubmissionStatus.ACCEPTED,
        )
        .exclude(id=submission.id)
        .exists()
    )

    is_accepted = submission.status == SubmissionStatus.ACCEPTED

    if is_accepted and not has_already_scored:
        submission.author.score += task.score
        submission.author.save()


def handle_uploaded_file(
    request: HttpRequest, task_id: int, submission_id: int
) -> None:
    submission: Submission = Submission._default_manager.get(id=submission_id)
    destination_dir = "apps/tasks/uploads/"
    os.makedirs(destination_dir, exist_ok=True)

    uploaded_file = request.FILES.get("file")

    if uploaded_file:
        with open(
            os.path.join(destination_dir, uploaded_file.name or ""), "wb+"
        ) as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        submission.status = SubmissionStatus.WAITING_JUDGE
        submission.save()


class DetailView(FormMixinBase, DetailViewBase):
    model = Task
    template_name = "tasks/detail.html"
    form_class = SubmissionForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = SubmissionForm()

        return context

    def get_success_url(self) -> str:
        return reverse("submissions:list")

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        self.object = self.get_object()

        if not self.object.is_accessible:
            return redirect("home")

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request: HttpRequest, *, pk: int) -> HttpResponse:
        # Unauthenticated users should not be able to submit
        # a submission to a task, so we redirect them to the
        # login page.
        if not request.user.is_authenticated:
            return redirect("login")

        self.object = self.get_object()
        form = self.get_form()
        uploaded_file = request.FILES.get("file")

        if not form.is_valid() and not uploaded_file:
            return self.form_invalid(form)

        submission = Submission._default_manager.create(
            code=form.cleaned_data.get("code", ""),
            task=self.object,
            author=request.user,
        )

        handle_submission.delay(
            form.cleaned_data.get("code", ""),
            self.object.id,
            submission.id,
        )

        if uploaded_file:
            upload_form = UploadFileForm(request.POST, request.FILES)
            if upload_form.is_valid():
                handle_uploaded_file(request, self.object.id, submission.id)

        return redirect(self.get_success_url())

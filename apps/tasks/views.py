import sys
from io import StringIO
from resource import RLIMIT_AS, getrlimit, setrlimit
from signal import SIGALRM, alarm, signal
from typing import TYPE_CHECKING, Any, Dict, Optional

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from apps.submissions.forms import SubmissionForm
from apps.submissions.models import Submission, SubmissionStatus
from apps.tasks.models import Task
from server import celery

if TYPE_CHECKING:
    DetailViewBase = generic.DetailView[Task]
    FormMixinBase = FormMixin[SubmissionForm]
else:
    DetailViewBase = generic.DetailView
    FormMixinBase = FormMixin


def signal_handler(signum: int, frame: object) -> None:
    raise TimeoutError("Time limit exceeded")


@celery.task(ignore_result=True)
def handle_submission(code: str, task_id: int, submission_id: int) -> None:
    task = Task._default_manager.get(id=task_id)
    submission = Submission._default_manager.get(id=submission_id)

    if task.memory_limit is not None:
        _, hard = getrlimit(RLIMIT_AS)
        setrlimit(RLIMIT_AS, (task.memory_limit, hard))

    if task.time_limit is not None:
        signal(SIGALRM, signal_handler)
        alarm(task.time_limit)

    if (output := compile_code(submission, task, code)) is None:
        return

    check_answer(submission, task, output)


def compile_code(
    submission: Submission, task: Task, code: str
) -> Optional[str]:
    input_data = StringIO(task.input_file)

    sys.stdin = input_data
    sys.stdout = stdout = StringIO()

    try:
        eval(compile(code, "<string>", "exec"))
    except MemoryError:  # pragma: no cover
        submission.status = "MLE"
        submission.save()
        return None
    except TimeoutError:  # pragma: no cover
        submission.status = "TLE"
        submission.save()
        return None
    except Exception:
        submission.status = "RE"
        submission.save()
        return None

    return stdout.getvalue()


def check_answer(submission: Submission, task: Task, output: str) -> None:
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

        if not form.is_valid():
            return self.form_invalid(form)

        submission = Submission._default_manager.create(
            code=form.cleaned_data["code"],
            task=self.object,
            author=request.user,
        )

        handle_submission.delay(
            form.cleaned_data["code"],
            self.object.id,
            submission.id,
        )

        return redirect(self.get_success_url())

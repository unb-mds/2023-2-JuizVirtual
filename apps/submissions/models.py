from django.core.validators import MinLengthValidator
from django.db.models import CASCADE, ForeignKey, TextChoices, TextField
from django.utils.translation import gettext_lazy as _

from apps.tasks.models import Task
from apps.users.models import User
from core.models import TimestampedModel


class SubmissionStatus(TextChoices):
    """Represents the status of a submission."""

    WAITING_JUDGE = ("WJ", _("Waiting judge"))
    JUDGING = ("JG", _("Judging"))
    ACCEPTED = ("AC", _("Accepted"))
    WRONG_ANSWER = ("WA", _("Wrong answer"))
    RUNTIME_ERROR = ("RE", _("Runtime error"))
    TIME_LIMIT_EXCEEDED = ("TLE", _("Time limit exceeded"))
    MEMORY_LIMIT_EXCEEDED = ("MLE", _("Memory limit exceeded"))
    COMPILATION_ERROR = ("CE", _("Compilation error"))
    INTERNAL_ERROR = ("IE", _("Internal error"))
    UNKNOWN_ERROR = ("UE", _("Unknown error"))
    SUBMISSION_ERROR = ("SE", _("Submission error"))
    PRESENTATION_ERROR = ("PE", _("Presentation error"))


class Submission(TimestampedModel):
    """
    Represents a submission to a task by an user. The code field is
    validated to have at least 15 characters and if it is a valid Python
    code.
    """

    author = ForeignKey(User, related_name="submissions", on_delete=CASCADE)
    task = ForeignKey(Task, related_name="submissions", on_delete=CASCADE)
    code = TextField(validators=[MinLengthValidator(15)])
    status = TextField(
        max_length=3,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.WAITING_JUDGE,
    )

    class Meta:
        db_table = "submissions"

    def __str__(self) -> str:
        return f"#{self.id}"

from django.core.validators import MinLengthValidator
from django.db.models import CASCADE, ForeignKey, TextField

from apps.tasks.models import Task
from apps.users.models import User
from core.models import TimestampedModel


class Submission(TimestampedModel):
    """
    Represents a submission to a task by an user. The code field is
    validated to have at least 15 characters and if it is a valid Python
    code.
    """

    author = ForeignKey(User, related_name="submissions", on_delete=CASCADE)
    task = ForeignKey(Task, related_name="submissions", on_delete=CASCADE)
    code = TextField(validators=[MinLengthValidator(15)])

    class Meta:
        db_table = "submissions"

    def __str__(self) -> str:
        return f"#{self.id}"

from django.db.models import CASCADE, ForeignKey, TextField

from apps.tasks.models import Task
from apps.users.models import User
from core.models import TimestampedModel


class Submission(TimestampedModel):
    id: int

    author = ForeignKey(User, related_name="submissions", on_delete=CASCADE)
    task = ForeignKey(Task, related_name="submissions", on_delete=CASCADE)
    code = TextField()

    class Meta:
        db_table = "submissions"

    def __str__(self) -> str:
        return f"{self.code} #{self.id}"

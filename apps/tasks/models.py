from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    IntegerField,
    TextField,
)

from apps.contests.enums import ContestStatus
from apps.contests.models import Contest
from core.models import TimestampedModel


class Task(TimestampedModel):
    """Represents a task in a contest."""

    title = CharField(max_length=256)
    description = CharField(max_length=4096)
    constraints = ArrayField(CharField(max_length=256), default=list)

    contest = ForeignKey(Contest, related_name="tasks", on_delete=CASCADE)
    score = IntegerField(null=True)

    memory_limit = IntegerField(null=True)
    time_limit = IntegerField(null=True)

    input_file = TextField(default="")
    output_file = TextField(default="")

    class Meta:
        db_table = "tasks"

    def __str__(self) -> str:
        return self.title

    @property
    def is_accessible(self) -> bool:
        return self.contest.status in (
            ContestStatus.RUNNING,
            ContestStatus.FINISHED,
        )

from django.db.models import CASCADE, CharField, ForeignKey, IntegerField

from apps.contests.enums import ContestStatus
from apps.contests.models import Contest
from core.models import TimestampedModel


class Problem(TimestampedModel):
    """Represents a problem in a contest."""

    title = CharField(max_length=256)
    description = CharField(max_length=4096)

    contest = ForeignKey(Contest, related_name="problems", on_delete=CASCADE)
    score = IntegerField(null=True)

    memory_limit = IntegerField(null=True)
    time_limit = IntegerField(null=True)

    class Meta:
        db_table = "problems"

    def __str__(self) -> str:
        return self.title

    @property
    def is_accessible(self) -> bool:
        return self.contest.status in (
            ContestStatus.RUNNING,
            ContestStatus.FINISHED,
        )

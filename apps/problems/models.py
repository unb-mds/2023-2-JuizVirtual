from django.db.models import CASCADE, CharField, ForeignKey

from apps.contests.models import Contest
from core.models import TimestampedModel


class Problem(TimestampedModel):
    """Represents a problem in a contest."""

    title = CharField(max_length=256)
    description = CharField(max_length=4096)

    contest = ForeignKey(Contest, related_name="problems", on_delete=CASCADE)

    class Meta:
        db_table = "problems"

    def __str__(self) -> str:
        return self.title

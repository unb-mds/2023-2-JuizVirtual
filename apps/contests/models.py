from typing import Any

from django.core.exceptions import ValidationError
from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    ManyToManyField,
)
from django.utils.timezone import now

from apps.contests.enums import ContestStatus
from apps.users.models import User
from core.models import TimestampedModel


class Contest(TimestampedModel):
    """Represents a contest."""

    id: int

    title = CharField(max_length=256)
    description = CharField(max_length=1024)

    start_time = DateTimeField()
    end_time = DateTimeField()
    cancelled = BooleanField(default=False)

    users = ManyToManyField(User, related_name="contests")

    class Meta:
        db_table = "contests"

    def __str__(self) -> str:
        return f"{self.title} #{self.id}"

    @property
    def status(self) -> ContestStatus:
        if self.cancelled:
            return ContestStatus.CANCELLED

        if self.start_time > now():
            return ContestStatus.PENDING
        elif self.end_time < now():
            return ContestStatus.FINISHED
        else:
            return ContestStatus.RUNNING

    def clean(self) -> Any:
        super().clean()

        if self.start_time > self.end_time:
            raise ValidationError("Start time must be before end time.")

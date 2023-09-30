from django.db.models import CharField, DateTimeField, ManyToManyField

from apps.users.models import User
from core.models import TimestampedModel


class Contest(TimestampedModel):
    """Represents a contest."""

    id: int

    title = CharField(max_length=256)
    description = CharField(max_length=1024)

    start_time = DateTimeField()
    end_time = DateTimeField()

    users = ManyToManyField(User, related_name="contests")

    class Meta:
        db_table = "contests"

    def __str__(self) -> str:
        return f"{self.title} #{self.id}"

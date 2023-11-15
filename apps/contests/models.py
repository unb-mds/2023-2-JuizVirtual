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
        """
        Retorna o status atual do contest baseado no horário atual.

        .. list-table:: Status do contest
            :header-rows: 1

        * - Status
          - Descrição
        * - :attr:`ContestStatus.PENDING`
          - Quando o contest ainda não começou.
        * - :attr:`ContestStatus.RUNNING`
          - Quando o contest está acontecendo.
        * - :attr:`ContestStatus.FINISHED`
          - Quando o contest já terminou.
        * - :attr:`ContestStatus.CANCELLED`
          - Quando o contest foi cancelado.

        Returns
        -------
        :class:`ContestStatus`
            O status atual do contest.
        """
        if self.cancelled:
            return ContestStatus.CANCELLED
        elif self.start_time > now():
            return ContestStatus.PENDING
        elif self.end_time < now():
            return ContestStatus.FINISHED
        else:
            return ContestStatus.RUNNING

    def clean(self) -> None:
        """
        Validação do contest. Verifica se o :attr:`start_time` é menor
        que o :attr:`end_time`, ou seja, se o contest começa antes de
        terminar. Se não for, lança um :class:`ValidationError`.

        Raises
        ------
        :class:`ValidationError`
            Se o :attr:`start_time` for maior que o :attr:`end_time`.
        """
        if self.start_time > self.end_time:
            raise ValidationError("Start time must be before end time.")

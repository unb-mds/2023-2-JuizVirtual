from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.contests.enums import ContestStatus
from apps.contests.models import Contest


class ContestModelFormTestCase(TestCase):
    def setUp(self) -> None:
        now = timezone.now()
        self.contest = Contest(
            id=1,
            title="Test Contest",
            description="This is a test contest",
            start_time=now,
            end_time=now + timedelta(hours=1),
            cancelled=False,
        )

    def test_status_pending(self) -> None:
        self.contest.start_time = timezone.now() + timedelta(hours=1)
        self.assertEqual(self.contest.status, ContestStatus.PENDING)

    def test_status_running(self) -> None:
        self.contest.start_time = timezone.now() - timedelta(hours=1)
        self.contest.end_time = timezone.now() + timedelta(hours=1)
        self.assertEqual(self.contest.status, ContestStatus.RUNNING)

    def test_status_finished(self) -> None:
        self.contest.end_time = timezone.now() - timedelta(hours=1)
        self.assertEqual(self.contest.status, ContestStatus.FINISHED)

    def test_status_cancelled(self) -> None:
        self.contest.cancelled = True
        self.assertEqual(self.contest.status, ContestStatus.CANCELLED)


class TestContestStatus(TestCase):
    def test_pending(self) -> None:
        self.assertEqual(ContestStatus.PENDING, "Pending")

    def test_running(self) -> None:
        self.assertEqual(ContestStatus.RUNNING, "Running")

    def test_finished(self) -> None:
        self.assertEqual(ContestStatus.FINISHED, "Finished")

    def test_cancelled(self) -> None:
        self.assertEqual(ContestStatus.CANCELLED, "Cancelled")

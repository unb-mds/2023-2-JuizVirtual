from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.contests.models import Contest
from apps.submissions.models import Submission
from apps.tasks.models import Task
from apps.users.models import User


class SubmissionTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            is_active=True,
            is_staff=False,
        )

        self.contest = Contest(
            title="Test Contest",
            description="This is a test contest",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            cancelled=False,
        )

        self.task = Task(contest=self.contest)

        self.submission = Submission(
            author=self.user, task=self.task, code="this is some code"
        )

    def test_submission_str_code(self) -> None:
        self.assertEqual(str(self.submission.code), "this is some code")

    def test_submission_author_relationship(self) -> None:
        self.assertEqual(self.submission.author, self.user)

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.contests.models import Contest
from apps.submissions.models import Submission
from apps.tasks.models import Task
from apps.users.models import User


class SubmissionTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="user",
            email="user@email.com",
            password="password",
        )
        self.contest = Contest._default_manager.create(
            title="Test Contest",
            description="This is a test contest",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            cancelled=False,
        )
        self.task = Task._default_manager.create(
            title="Test Task",
            description="This is a test task",
            contest=self.contest,
        )
        self.submission = Submission(
            author=self.user,
            task=self.task,
            code="print('hello world')",
        )

    def test_submission_representation(self) -> None:
        expected = f"#{self.submission.id}"
        self.assertEqual(str(self.submission), expected)

    def test_submission_has_author_relationship(self) -> None:
        self.assertEqual(self.submission.author, self.user)

    def test_submission_has_task_relationship(self) -> None:
        self.assertEqual(self.submission.task, self.task)

    def test_submission_code_min_length_validator(self) -> None:
        code = "a" * 14
        submission = Submission(author=self.user, task=self.task, code=code)

        expected = [
            "Ensure this value has at least 15 characters (it has 14)."
        ]

        with self.assertRaises(ValidationError) as context:
            submission.full_clean()

        self.assertEqual(context.exception.messages, expected)

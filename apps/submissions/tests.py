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
            email="user@example",
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

        self.code = "print('hello world')"

    def test_create_submission(self) -> None:
        submission = Submission._default_manager.create(
            author=self.user,
            task=self.task,
            code=self.code,
        )

        self.assertEqual(submission.author, self.user)
        self.assertEqual(submission.task, self.task)
        self.assertEqual(submission.code, self.code)

    def test_submission_representation(self) -> None:
        submission = Submission._default_manager.create(
            author=self.user,
            task=self.task,
            code=self.code,
        )

        expected = f"#{submission.id}"
        self.assertEqual(str(submission), expected)

    def test_submission_code_min_length_validator(self) -> None:
        code = "a" * 14
        submission = Submission(
            author=self.user,
            task=self.task,
            code=code,
        )

        expected = [
            "Ensure this value has at least 15 characters (it has 14)."
        ]

        with self.assertRaises(ValidationError) as context:
            submission.full_clean()

        self.assertEqual(context.exception.messages, expected)

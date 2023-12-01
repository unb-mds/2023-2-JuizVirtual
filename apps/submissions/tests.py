from datetime import timedelta

from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.contests.models import Contest
from apps.submissions.admin import SubmissionAdmin
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


class SubmissionAdminTest(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.submission_admin = SubmissionAdmin(Submission, self.site)

    def test_list_display(self) -> None:
        expected = ("__str__", "author", "task")
        self.assertEqual(self.submission_admin.list_display, expected)

    def test_list_filter(self) -> None:
        expected = ("author", "task", "created_at")
        self.assertEqual(self.submission_admin.list_filter, expected)

    def test_fieldsets(self) -> None:
        expected = [
            (_("Details"), {"fields": ("author", "task", "code", "status")})
        ]
        self.assertEqual(self.submission_admin.fieldsets, expected)


class SubmissionListViewtest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example",
            password="testpassword",
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

        self.submission = Submission._default_manager.create(
            author=self.user,
            task=self.task,
            code="test code",
        )

    def test_submission_list_view(self) -> None:
        self.client.login(email="testuser@example", password="testpassword")

        url = reverse("submissions:list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("submissions", response.context)
        self.assertIn(self.submission, response.context["submissions"])

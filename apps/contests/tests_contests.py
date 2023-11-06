import unittest
from datetime import timedelta

from django.contrib.admin import AdminSite
from django.forms import CharField, Textarea
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from apps.contests.admin import ContestAdmin, ContestModelForm
from apps.contests.enums import ContestStatus
from apps.contests.models import Contest


class ContestTestCase(TestCase):
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


class ContestStatusTesteCase(TestCase):
    def test_pending(self) -> None:
        self.assertEqual(ContestStatus.PENDING, "Pending")

    def test_running(self) -> None:
        self.assertEqual(ContestStatus.RUNNING, "Running")

    def test_finished(self) -> None:
        self.assertEqual(ContestStatus.FINISHED, "Finished")

    def test_cancelled(self) -> None:
        self.assertEqual(ContestStatus.CANCELLED, "Cancelled")


class ContestModelFormTestCase(TestCase):
    def test_description_field_widget(self) -> None:
        form = ContestModelForm()
        description_field = form.fields["description"]

        self.assertIsInstance(description_field, CharField)

        self.assertIsInstance(description_field.widget, Textarea)
        self.assertEqual(
            description_field.widget.attrs, {"rows": 14, "cols": 80}
        )

    def test_model_and_fields(self) -> None:
        form = ContestModelForm()

        self.assertEqual(form._meta.model, Contest)


class ContestAdminTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.contest_admin = ContestAdmin(Contest, self.site)

    def test_list_display(self) -> None:
        expected_list_display = ("title", "start_time", "end_time", "status")
        self.assertEqual(
            self.contest_admin.list_display, expected_list_display
        )

    def test_list_filter(self) -> None:
        expected_list_filter = ("start_time", "end_time")
        self.assertEqual(self.contest_admin.list_filter, expected_list_filter)

    def test_fieldsets(self) -> None:
        expected_fieldsets = [
            (("General"), {"fields": ("title", "description")}),
            (("Other"), {"fields": ("start_time", "end_time", "cancelled")}),
        ]
        self.assertEqual(self.contest_admin.fieldsets, expected_fieldsets)


class ContestsUrlsTestCase(TestCase):
    def test_detail_url_resolves(self) -> None:
        url = reverse("contests:detail", args=[1])
        resolved_view_name = resolve(url).view_name
        expected_view_name = "contests:detail"

        self.assertEqual(resolved_view_name, expected_view_name)


class ContestViewsTesteCase(TestCase):
    # tentar novamente depois
    pass

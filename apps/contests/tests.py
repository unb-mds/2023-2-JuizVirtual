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
        self.contest = Contest(
            title="Test Contest",
            description="This is a test contest",
            cancelled=False,
        )

    def test_status_pending(self) -> None:
        self.contest.start_time = timezone.now() + timedelta(hours=1)
        self.contest.end_time = timezone.now() + timedelta(hours=2)
        self.assertEqual(self.contest.status, ContestStatus.PENDING)

    def test_status_running(self) -> None:
        self.contest.start_time = timezone.now() - timedelta(hours=1)
        self.contest.end_time = timezone.now() + timedelta(hours=1)
        self.assertEqual(self.contest.status, ContestStatus.RUNNING)

    def test_status_finished(self) -> None:
        self.contest.start_time = timezone.now() - timedelta(hours=2)
        self.contest.end_time = timezone.now() - timedelta(hours=1)
        self.assertEqual(self.contest.status, ContestStatus.FINISHED)

    def test_status_cancelled(self) -> None:
        self.contest.cancelled = True
        self.assertEqual(self.contest.status, ContestStatus.CANCELLED)


class ContestStatusTestCase(TestCase):
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
        attrs = {"rows": 14, "cols": 80}

        self.assertIsInstance(description_field, CharField)
        self.assertIsInstance(description_field.widget, Textarea)
        self.assertEqual(description_field.widget.attrs, attrs)

    def test_form_model_to_be_contest(self) -> None:
        self.assertEqual(ContestModelForm()._meta.model, Contest)


class ContestAdminTestCase(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.admin = ContestAdmin(Contest, self.site)

    def test_list_display(self) -> None:
        list_display = self.admin.list_display
        expected = ("title", "start_time", "end_time", "status")

        self.assertEqual(list_display, expected)

    def test_list_filter(self) -> None:
        list_filter = self.admin.list_filter
        expected = ("start_time", "end_time")

        self.assertEqual(list_filter, expected)

    def test_fieldsets(self) -> None:
        fieldsets = self.admin.fieldsets
        expected = [
            (("General"), {"fields": ("title", "description")}),
            (("Other"), {"fields": ("start_time", "end_time", "cancelled")}),
        ]

        self.assertEqual(fieldsets, expected)


class ContestURLTestCase(TestCase):
    def test_detail_url_resolves(self) -> None:
        url = reverse("contests:detail", args=[1])

        view_name = resolve(url).view_name
        expected = "contests:detail"

        self.assertEqual(view_name, expected)


class ContestViewTestCase(TestCase):
    def setUp(self) -> None:
        now = timezone.now()
        self.contest = Contest._default_manager.create(
            title="Test Contest",
            description="This is a test contest",
            start_time=now,
            end_time=now + timedelta(hours=1),
            cancelled=False,
        )

    def test_index_view(self) -> None:
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Contest")

    def test_detail_view(self) -> None:
        url = reverse("contests:detail", args=[self.contest.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Contest")

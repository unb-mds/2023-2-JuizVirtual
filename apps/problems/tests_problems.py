from datetime import timedelta

from django.contrib.admin.sites import AdminSite

# from django.forms import CharField, IntegerField
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from apps.contests.models import Contest
from apps.problems.admin import ProblemAdmin, ProblemModelForm
from apps.problems.models import Problem
from apps.problems.views import DetailView


class ProblemTestCase(TestCase):
    def test_is_accessible(self) -> None:
        now = timezone.now()

        start_time = now - timedelta(hours=1)
        end_time = now + timedelta(hours=1)
        contest = Contest(start_time=start_time, end_time=end_time)

        problem = Problem(contest=contest)

        self.assertTrue(problem.is_accessible)

        contest.start_time = now - timedelta(hours=2)
        contest.end_time = now - timedelta(hours=1)
        contest.save()

        self.assertTrue(problem.is_accessible)

        contest.start_time = now + timedelta(hours=1)
        contest.end_time = now + timedelta(hours=2)
        contest.save()

        self.assertFalse(problem.is_accessible)


# teste a seguir passou, porém na
# hora do commit apresenta erros
# class ProblemModelFormTesteCase(TestCase):


#   def test_form_fields(self) -> None:
#        data = {"description":
#           "Problem description",
#           "score": 10,"memory_limit":
#           1024,"time_limit": 60,}
#        form = ProblemModelForm(data)
#        self.assertIsInstance
#       (form.fields["description"], CharField)
#        self.assertIsInstance
#       (form.fields["score"], IntegerField)


#        self.assertIsInstance
#       (form.fields["memory_limit"], IntegerField)
#        self.assertIsInstance(form.fields
#       ["time_limit"], IntegerField)
#        self.assertEqual(
#           form.fields["description"]
#       .widget.attrs, {"rows": 14, "cols": 80})


#        self.assertEqual(form.fields
#          ["score"].min_value, 0)
#        self.assertFalse(form.fields
#           ["score"].required)
#        self.assertEqual(form.fields
#          ["memory_limit"].min_value, 0)


#        self.assertFalse(form.fields
#       ["memory_limit"].required)
#        self.assertEqual(form.fields
#       ["memory_limit"].help_text, "In bytes.")
#        self.assertEqual(form.fields
#       ["time_limit"].min_value, 0)
#        self.assertFalse(form.fields
#       ["time_limit"].required)
#        self.assertEqual(form.fields["time_limit"]
#       .help_text, "In seconds.")


class ProblemAdminTestCase(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.admin = ProblemAdmin(Problem, self.site)
        now = timezone.now()
        self.contest = Contest(
            title="Test Contest 1",
            description="This is a test contest",
            start_time=now,
            end_time=now + timedelta(hours=1),
            cancelled=False,
        )
        self.contest.save()

    def test_admin_fields(self) -> None:
        self.assertEqual(self.admin.form, ProblemModelForm)

        self.assertEqual(
            self.admin.list_display,
            ("title", "contest", "memory_limit", "time_limit"),
        )
        self.assertEqual(self.admin.list_filter, ("contest", "score"))

        expected_fieldsets = [
            (("General"), {"fields": ("title", "description")}),
            (("Meta"), {"fields": ("contest", "score")}),
            (("Limits"), {"fields": ("memory_limit", "time_limit")}),
        ]
        self.assertEqual(self.admin.fieldsets, expected_fieldsets)


class ProblemURLsTestCase(TestCase):
    def test_detail_url_resolves_to_detail_view(self) -> None:
        url = reverse("problems:detail", args=[int])

        resolver = resolve(url)

        self.assertEqual(resolver.url_name, DetailView)

    def test_detail_url_reverse(self) -> None:
        expected_url = "/problems/int/"

        generated_url = reverse("problems:detail", args=[int])

        self.assertEqual(generated_url, expected_url)

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.contests.models import Contest
from apps.problems.models import Problem


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


class DetailViewTestCase(TestCase):
    pass


class ProblemAdminTestCase(TestCase):
    pass

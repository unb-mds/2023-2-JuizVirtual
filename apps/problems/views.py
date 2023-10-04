from typing import TYPE_CHECKING

from django.views import generic

from apps.problems.models import Problem

if TYPE_CHECKING:
    DetailViewBase = generic.DetailView[Problem]
else:
    DetailViewBase = generic.DetailView


class DetailView(DetailViewBase):
    model = Problem
    template_name = "problems/detail.html"

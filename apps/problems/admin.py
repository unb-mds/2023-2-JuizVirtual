from typing import TYPE_CHECKING

from django.contrib.admin import ModelAdmin, register
from django.forms import CharField, ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

from apps.problems.models import Problem

if TYPE_CHECKING:
    ProblemAdminBase = ModelAdmin[Problem]
    ProblemModelFormBase = ModelForm[Problem]
else:
    ProblemAdminBase = ModelAdmin
    ProblemModelFormBase = ModelForm


class ProblemModelForm(ProblemModelFormBase):
    description = CharField(widget=Textarea(attrs={"rows": 14, "cols": 80}))

    class Meta:
        model = Problem
        fields = "__all__"


@register(Problem)
class ProblemAdmin(ProblemAdminBase):
    form = ProblemModelForm

    fieldsets = [
        (_("Problem"), {"fields": ("title", "description", "contest")}),
    ]

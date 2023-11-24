from typing import TYPE_CHECKING

from django.contrib.admin import ModelAdmin, register
from django.forms import CharField, ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

from apps.submissions.models import Submission

if TYPE_CHECKING:
    SubmissionAdminBase = ModelAdmin[Submission]
    SubmissionModelFormBase = ModelForm[Submission]
else:
    SubmissionAdminBase = ModelAdmin
    SubmissionModelFormBase = ModelForm


class SubmissionModelForm(SubmissionModelFormBase):
    submission_data = CharField(
        widget=Textarea(attrs={"rows": 10, "cols": 80})
    )

    class Meta:
        model = Submission
        fields = "__all__"


@register(Submission)
class SubmissionAdmin(SubmissionAdminBase):
    form = SubmissionModelForm

    list_display = ("author", "task")
    list_filter = ("task",)
    search_fields = ("author__username", "task__title")

    fieldsets = [
        (
            _("Submission Details"),
            {"fields": ("author", "task", "code")},
        )
    ]

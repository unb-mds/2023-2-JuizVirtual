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
    code = CharField(widget=Textarea(attrs={"rows": 20, "cols": 80}))

    class Meta:
        model = Submission
        fields = "__all__"


@register(Submission)
class SubmissionAdmin(SubmissionAdminBase):
    form = SubmissionModelForm

    list_display = ("__str__", "author", "task")
    list_filter = ("author", "task", "created_at")

    fieldsets = [
        (_("Details"), {"fields": ("author", "task", "code", "status")})
    ]

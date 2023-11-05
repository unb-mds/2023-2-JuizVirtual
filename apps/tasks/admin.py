from typing import TYPE_CHECKING

from django.contrib.admin import ModelAdmin, register
from django.forms import CharField, IntegerField, ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

from apps.tasks.models import Task

if TYPE_CHECKING:
    TaskAdminBase = ModelAdmin[Task]
    TaskModelFormBase = ModelForm[Task]
else:
    TaskAdminBase = ModelAdmin
    TaskModelFormBase = ModelForm


class TaskModelForm(TaskModelFormBase):
    description = CharField(widget=Textarea(attrs={"rows": 14, "cols": 80}))
    score = IntegerField(min_value=0, required=False)

    memory_limit = IntegerField(
        min_value=0, required=False, help_text=_("In bytes.")
    )
    time_limit = IntegerField(
        min_value=0, required=False, help_text=_("In seconds.")
    )

    class Meta:
        model = Task
        fields = "__all__"


@register(Task)
class TaskAdmin(TaskAdminBase):
    form = TaskModelForm

    list_display = ("title", "contest", "memory_limit", "time_limit")
    list_filter = ("contest", "score")

    fieldsets = [
        (_("General"), {"fields": ("title", "description")}),
        (_("Meta"), {"fields": ("contest", "score")}),
        (_("Limits"), {"fields": ("memory_limit", "time_limit")}),
    ]

from typing import TYPE_CHECKING, cast

from django.contrib.admin import ModelAdmin, register
from django.contrib.postgres.forms import SimpleArrayField
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import (
    CharField,
    FileField,
    IntegerField,
    ModelForm,
    Textarea,
)
from django.http import HttpRequest
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
    constraints = SimpleArrayField(CharField(max_length=256), required=False)
    score = IntegerField(min_value=0, required=False)

    memory_limit = IntegerField(
        min_value=0,
        required=False,
        help_text=_("In bytes."),
    )
    time_limit = IntegerField(
        min_value=0,
        required=False,
        help_text=_("In seconds."),
    )

    input_file = FileField()
    output_file = FileField()

    class Meta:
        model = Task
        fields = "__all__"


@register(Task)
class TaskAdmin(TaskAdminBase):
    form = TaskModelForm

    list_display = ("title", "contest", "memory_limit", "time_limit")
    list_filter = ("contest", "score")

    fieldsets = [
        (_("General"), {"fields": ("title", "description", "constraints")}),
        (_("Meta"), {"fields": ("contest", "score")}),
        (_("Limits"), {"fields": ("memory_limit", "time_limit")}),
        (_("Test case"), {"fields": ("input_file", "output_file")}),
    ]

    def save_model(
        self,
        request: HttpRequest,
        obj: Task,
        form: TaskModelForm,
        change: bool,
    ) -> None:
        if change and len(request.FILES) == 0:
            return super().save_model(request, obj, form, change)

        try:
            # request.FILES does not cast to the correct type so we need
            # to cast it manually, otherwise Mypy will complain.
            input_file = cast(
                InMemoryUploadedFile, request.FILES["input_file"]
            )
            output_file = cast(
                InMemoryUploadedFile, request.FILES["output_file"]
            )
        except KeyError:
            return super().save_model(request, obj, form, change)

        obj.input_file = input_file.read().decode("utf-8")
        obj.output_file = output_file.read().decode("utf-8")

        return super().save_model(request, obj, form, change)

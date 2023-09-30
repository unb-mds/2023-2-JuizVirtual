from typing import TYPE_CHECKING

from django.contrib.admin import ModelAdmin, register
from django.utils.translation import gettext_lazy as _

from apps.contests.models import Contest

if TYPE_CHECKING:
    ContestAdminBase = ModelAdmin[Contest]
else:
    ContestAdminBase = ModelAdmin


@register(Contest)
class ContestAdmin(ContestAdminBase):
    list_display = ("title", "start_time", "status")
    list_filter = ("start_time", "end_time")
    fieldsets = [
        (_("General"), {"fields": ("title", "description")}),
        (_("Other"), {"fields": ("start_time", "end_time", "users")}),
    ]

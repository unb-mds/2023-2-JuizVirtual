from django.contrib.admin import ModelAdmin, register
from django.utils.translation import gettext_lazy as _

from apps.contests.models import Contest


@register(Contest)
class ContestAdmin(ModelAdmin[Contest]):
    list_display = ("title", "start_time", "end_time")
    fieldsets = [
        (_("General"), {"fields": ("title", "description")}),
        (_("Other"), {"fields": ("start_time", "end_time", "users")}),
    ]

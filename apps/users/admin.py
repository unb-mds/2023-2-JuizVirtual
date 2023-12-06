from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


@register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "score")
    fieldsets = [
        (
            _("Personal info"),
            {"fields": ("username", "email", "password", "score")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "user_permissions",
                    "groups",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    ]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "score",
                ),
            },
        ),
    )

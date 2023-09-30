from django.apps import AppConfig

default_app_config = "apps.users.UsersConfig"


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

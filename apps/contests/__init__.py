from django.apps import AppConfig

default_app_config = "apps.contests.ContestsConfig"


class ContestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.contests"

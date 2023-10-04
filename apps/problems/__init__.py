from django.apps import AppConfig

default_app_config = "apps.problems.ProblemsConfig"


class ProblemsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.problems"

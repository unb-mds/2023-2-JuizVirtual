from django.apps import AppConfig

default_app_config = "apps.submissions.SubmissionsConfig"


class SubmissionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.submissions"

from django.apps import AppConfig

default_app_config = "apps.tasks.TasksConfig"


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tasks"

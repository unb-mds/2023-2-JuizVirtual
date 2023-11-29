from os import environ

from celery import Celery
from celery.app.task import Task

from server.settings import env

environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings.development")

broker = env("CLOUDAMQP_URL", default="")
app = Celery(
    "virtualjudge", broker=broker, broker_connection_retry_on_startup=False
)

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# We are monkey-patching to add type hints to Celery. This is not a good
# practice of course, but it is a workaround for now, since Celery does
# not support type hints yet and this project is just an academic
# project.
# If you don't know what "monkey-patching" is, please read this:
# https://en.wikipedia.org/wiki/Monkey_patch
class_getitem = classmethod(lambda cls, *args, **kwargs: cls)
Task.__class_getitem__ = class_getitem  # type: ignore[attr-defined]

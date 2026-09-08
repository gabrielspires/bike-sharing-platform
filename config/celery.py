import os

from celery import Celery
from decouple import config

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    config("DJANGO_SETTINGS_MODULE"),
)

app = Celery("bike_sharing_platform")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_ai_project.settings")

app = Celery("music_ai_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

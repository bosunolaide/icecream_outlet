
import os
from celery import Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "icecream_outlet.settings")
app = Celery("icecream_outlet")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

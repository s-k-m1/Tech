import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("sk_tech")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "run-security-scan-every-5-minutes": {
        "task": "apps.core.tasks.security_tasks.run_security_scan",
        "schedule": 300.0,
    },
}

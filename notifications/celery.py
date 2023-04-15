import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

app = Celery('task_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    {
        'task_routes': {
            'send_push': {'queue': 'send_push'},
        }
    }
)

app.autodiscover_tasks()

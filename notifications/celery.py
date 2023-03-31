import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

app = Celery('task_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    {
        'task_routes': {
            'send_push': {'queue': 'send_push'},
            'update_exchange_rates': {'queue': 'update_exchange_rates'},
        }
    }
)

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'update_exchange_rates': {
#         'task': 'finance.tasks.update_exchange_rates',
#         'schedule': crontab(hour=12, minute=30),
#     },
# }

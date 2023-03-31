from django_celery_beat.models import PeriodicTask, ClockedSchedule
import json


def create_periodic_task(notification):
    clocked = ClockedSchedule.objects.create(clocked_time=notification.launch_time)
    PeriodicTask.objects.create(
        clocked=clocked,
        name=f'notification# {notification.id}: {notification.name}',
        task='notifications.tasks.send_push',
        enabled=True,
        one_off=True,
        kwargs=json.dumps(
            {
                'message_body': 'notification.name',
                'fca_token': 'fca_token',
                'notification_id': notification.id
            }
        )
    )

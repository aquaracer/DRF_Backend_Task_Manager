import os, requests, json

from .celery import app
from .models import Notification


@app.task(
    bind=True,
    soft_time_limit=os.getenv('CELERY_TASK_TIMEOUT', 300),
    default_retry_delay=os.getenv('CELERY_TASK_RETRY_TIME', 30),
    queue='send_push'
)
def send_push(self, message_body=None, fca_token=None, notification_id=None):
    """Отправка PUSH уведомления пользователю"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key=' + os.getenv('FIREBASE_API_KEY')
    }
    payload = {
        "registration_ids": fca_token,
        "priority": "high",
        "notification": {
            "title": "TASK NOTIFICATION",
            "body": message_body,
        }
    }

    error_message = None

    try:
        response = requests.post(os.getenv('FIREBASE_SEND_NOTIFICATION_URL'), data=json.dumps(payload), headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        error_message = err
    except requests.exceptions.HTTPError as errh:
        error_message = errh
    except requests.exceptions.ConnectionError as errc:
        error_message = errc
    except requests.exceptions.Timeout as errt:
        error_message = errt

    if error_message is not None:
        Notification.objects.filter(id=notification_id).update(
            status=Notification.ERROR,
            error_text=error_message
        )
    else:
        Notification.objects.filter(id=notification_id).update(
            status=Notification.COMPLETED,
            task_result_id=self.request.id
        )

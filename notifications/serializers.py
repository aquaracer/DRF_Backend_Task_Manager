from rest_framework import serializers

from .models import Notification
from notifications.services import create_periodic_task


class NotificationSerializer(serializers.ModelSerializer):
    """Уведомление"""

    class Meta:
        model = Notification
        exclude = ('task',)


class CreateNotificationSerializer(serializers.ModelSerializer):
    """Создание уведомления"""

    class Meta:
        model = Notification
        fields = ('task', 'name', 'launch_time',)

    def create(self, validated_data):
        instance_notification = super(CreateNotificationSerializer, self).create(validated_data)
        create_periodic_task(instance_notification)


class UpdateNotificationSerializer(serializers.ModelSerializer):
    """Изменение уведомления"""

    class Meta:
        model = Notification
        fields = ('name', 'launch_time',)

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from notifications.services import create_periodic_task

from .models import Task, Subtask, TaskLog
from notifications.models import Notification
from notifications.serializers import NotificationSerializer

class SubtaskSerializer(serializers.ModelSerializer):
    """Подзадача"""

    class Meta:
        model = Subtask
        fields = ('id', 'name', 'status')


class CreateSubtaskSerializer(serializers.ModelSerializer):
    """Создать подзадачу"""

    class Meta:
        model = Subtask
        fields = ('name', 'status', 'task_id')


class TaskSerializer(serializers.ModelSerializer):
    """Задача"""

    notification = serializers.SerializerMethodField('get_notification')
    subtasks = serializers.SerializerMethodField('get_subtasks')

    class Meta:
        model = Task
        exclude = ('user',)
        depth = 1

    def get_notification(self, obj: Task):
        if Notification.objects.filter(task=obj).exists():
            return NotificationSerializer(Notification.objects.get(task=obj)).data

    def get_subtasks(self, obj: Task):
        if Subtask.objects.filter(task=obj).exists():
            return SubtaskSerializer(Subtask.objects.filter(task=obj), many=True).data


class CreateTaskSerializer(serializers.ModelSerializer):
    """Создание задачи"""

    notification = NotificationSerializer(write_only=True)
    subtasks = SubtaskSerializer(write_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        notification = validated_data.pop('notification', None)
        subtasks = validated_data.pop('subtasks', None)
        instance = super(CreateTaskSerializer, self).create(validated_data)
        TaskLog.objects.create(task=instance, status=instance.status)

        if notification:
            instance_notification = Notification.objects.create(**notification, task=instance)
            create_periodic_task(instance_notification)

        if subtasks:
            subtasks_batch = []
            for subtask in subtasks:
                subtasks_batch.append(Subtask(**subtask, task=instance))
            Subtask.objects.bulk_create(subtasks_batch)

        return instance


class UpdateTaskSerializer(serializers.ModelSerializer):
    """Изменение задачи"""

    class Meta:
        model = Task
        exclude = ('user', 'created', 'last_updated',)

    def update(self, instance, validated_data):
        # если обновляем имя в задаче, то и обновляем и имя в уведомлении
        if validated_data.get('name') and validated_data.get('name') != instance.name:
            Notification.objects.filter(task=instance).update(name=validated_data.get('name'))

        # если обновился статус
        if validated_data.get('status') and validated_data.get('status') != instance.status:
            TaskLog.objects.create(task=instance, status=instance.status)

        instance = super(UpdateTaskSerializer, self).update(instance, validated_data)
        return instance


class GoogleAuthSerializer(serializers.Serializer):
    """ Сериализация данных от Google
    """
    email = serializers.EmailField()
    token = serializers.CharField()

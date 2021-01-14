from rest_framework import serializers
from .models import Tasks, TaskChanges


class TasksSerializer(serializers.ModelSerializer):
    """Информация о задаче"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tasks
        fields = ('id', 'name', 'description', 'created', 'status', 'planned_finish', 'user')


class TaskChangesSerializer(serializers.ModelSerializer):
    """Измененная информация о задаче"""

    class Meta:
        model = TaskChanges
        fields = '__all__'

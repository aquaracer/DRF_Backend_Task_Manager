from rest_framework import serializers
from .models import Tasks, TaskChanges, Fields
from django.db.transaction import atomic


class TasksSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tasks
        fields = ('id', 'name', 'description', 'created', 'status', 'planned_finish', 'user')

    @atomic
    def update(self, instance, validated_data):
        update_fields = []
        for item in list(validated_data.keys()):
            if getattr(instance, item) != validated_data[item]:
                update_fields.append(item)
                setattr(instance, item, validated_data[item])
        fields = Fields.objects.filter(name__in=update_fields)
        task_id = Tasks.objects.get(pk=instance.id)
        note = TaskChanges.objects.create(changed_task=task_id,
                                          task_name=instance.name,
                                          task_description=instance.description,
                                          task_status=instance.status,
                                          task_planned_finish=instance.planned_finish)
        note.changed_fields.set(fields)
        instance.save()
        return instance


class Filtered_TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('status', 'planned_finish')


class TaskChangesSerializer(serializers.ModelSerializer):
    changed_fields = serializers.StringRelatedField(many=True)

    class Meta:
        model = TaskChanges
        fields = ('changed_task', 'change_created', 'task_name', 'task_description',
                  'task_status', 'task_planned_finish', 'changed_fields')

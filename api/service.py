from api.models import TaskChanges


def mark_task_change(serializer):
    new_object = serializer.save()
    TaskChanges.objects.create(changed_task=new_object,
                               task_name=new_object.name,
                               task_description=new_object.description,
                               task_status=new_object.status,
                               task_planned_finish=new_object.planned_finish)

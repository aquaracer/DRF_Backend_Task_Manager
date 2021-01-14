from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import TasksSerializer, TaskChangesSerializer
from .models import Tasks, TaskChanges
from .service import mark_task_change


class TasksViewSet(ModelViewSet):
    """CRUD информации о задаче"""

    queryset = Tasks.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TasksSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user)
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        planned_finish = self.request.query_params.get('planned_finish', None)
        if planned_finish is not None:
            queryset = queryset.filter(planned_finish=planned_finish)
        return queryset

    def perform_create(self, serializer):
        mark_task_change(serializer)

    def perform_update(self, serializer):
        mark_task_change(serializer)


class TaskChangesView(ListAPIView):
    """Вывод списка изменений задачи"""

    permission_classes = (IsAuthenticated,)
    serializer_class = TaskChangesSerializer

    def get_queryset(self):
        user = self.request.user
        task_id = self.kwargs['task_id']
        return TaskChanges.objects.filter(changed_task=task_id, changed_task__user=user).order_by('-change_created')



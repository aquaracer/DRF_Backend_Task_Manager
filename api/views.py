from .models import Tasks, TaskChanges
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView, Response
from .serializers import TasksSerializer, Filtered_TasksSerializer, TaskChangesSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class TasksViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(user=user)


class FilteredTasksView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, status=None, planned_finish=None):
        data = {'status': status, 'planned_finish': planned_finish}
        serializer = Filtered_TasksSerializer(data=data)
        if serializer.is_valid():
            tasks = Tasks.objects.filter(status=status, planned_finish=planned_finish,
                                         user=request.user).all()
            serializer = TasksSerializer(tasks, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TaskChangesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, task_id):
        get_object_or_404(Tasks, id=task_id, user=request.user)
        changes = TaskChanges.objects.filter(changed_task=task_id).order_by('change_created').all()
        serializer = TaskChangesSerializer(changes, many=True)
        return Response(serializer.data)

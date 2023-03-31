from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
import datetime

from core.services import check_google_auth
from core.serializers import TaskSerializer, CreateTaskSerializer, UpdateTaskSerializer, SubtaskSerializer, \
    CreateSubtaskSerializer, GoogleAuthSerializer
from core.models import Task, Subtask
from notifications.tasks import send_push
from task_manager.swagger_schema import TOKENS_PARAMETER


@method_decorator(name='create',
                  decorator=swagger_auto_schema(tags=['task'], **TOKENS_PARAMETER,
                                                operation_description='Создание задачи'))
@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      tags=['task'],
                      operation_description='Cписок задач', **TOKENS_PARAMETER))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      tags=['task'],
                      operation_description='Информация об отдельной задаче', **TOKENS_PARAMETER))
@method_decorator(name='partial_update',
                  decorator=swagger_auto_schema(
                      tags=['task'],
                      operation_description='Изменение информации о задаче', **TOKENS_PARAMETER))
@method_decorator(name='destroy',
                  decorator=swagger_auto_schema(
                      tags=['task'],
                      operation_description='Удаление задачи', **TOKENS_PARAMETER))
class TaskViewSet(ModelViewSet):
    """CRUD задачи"""

    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user,
            status=Task.IN_PROGRESS,
            execution_date__gtt=datetime.datetime.now()
        )

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TaskSerializer
        elif self.action == 'create':
            return CreateTaskSerializer
        elif self.action == 'partial_update':
            return UpdateTaskSerializer

    @swagger_auto_schema(method='GET', tags=['Task'],
                         serializer_class=TaskSerializer, **TOKENS_PARAMETER)
    @action(detail=False, methods=['GET'])
    def task_diary(self, request):
        """Дневник задач"""

        data = TaskSerializer(
            Task.objects.filter(
                user=self.request.user,
                status=Task.COMPLETED,
                execution_date__lt=datetime.datetime.now(),
                execution_date__gte=datetime.datetime.now() - datetime.timedelta(30)
            ),
            many=True
        ).data
        return Response(data=data)

    @swagger_auto_schema(method='GET', tags=['Task'], serializer_class=TaskSerializer, **TOKENS_PARAMETER)
    @action(detail=False, methods=['GET'])
    def recycle_bin(self, request):
        """Корзина"""

        data = TaskSerializer(
            Task.objects.filter(
                user=self.request.user,
                status=Task.DELETED,
                execution_date__gte=datetime.datetime.now() - datetime.timedelta(30)
            ),
            many=True
        ).data
        return Response(data=data)

    @swagger_auto_schema(method='PATCH', tags=['Task'], serializer_class=TaskSerializer, **TOKENS_PARAMETER)
    @action(detail=True, methods=['PATCH'])
    def move_to_bin(self, request, pk):
        """Переместить задачу в корзину"""

        Task.objects.filter(id=pk).update(status=Task.DELETED)
        return Response()

    @swagger_auto_schema(method='PATCH', tags=['Task'], serializer_class=TaskSerializer, **TOKENS_PARAMETER)
    @action(detail=True, methods=['PATCH'])
    def empty_trecycle_bin(self, request, pk):
        """Очистить корзину"""

        Task.objects.filter(user=self.request.user, status=Task.DELETED).delete()
        return Response()


@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      tags=['subtask'],
                      operation_description='Создание подзадачи', **TOKENS_PARAMETER))
@method_decorator(name='partial_update',
                  decorator=swagger_auto_schema(
                      tags=['subtask'],
                      operation_description='Изменение информации о подзадаче', **TOKENS_PARAMETER))
@method_decorator(name='destroy',
                  decorator=swagger_auto_schema(
                      tags=['subtask'],
                      operation_description='Удаление подзадачи', **TOKENS_PARAMETER))
class SubtaskViewSet(ModelViewSet):
    """CRUD подзадачи"""

    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Subtask.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTaskSerializer
        elif self.action == 'partial_update':
            return SubtaskSerializer


@api_view(["POST"])
def google_auth(request):
    """ Подтверждение авторизации через Google"""

    google_data = GoogleAuthSerializer(data=request.data)
    if google_data.is_valid():
        token = check_google_auth(google_data.data)
        return Response(token)
    else:
        raise AuthenticationFailed(code=403, detail='Bad token Google')

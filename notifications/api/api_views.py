from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from notifications.serializers import NotificationSerializer, CreateNotificationSerializer, UpdateNotificationSerializer
from notifications.models import Notification
from task_manager.swagger_schema import TOKENS_PARAMETER

@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      tags=['notification'],
                      operation_description='Создание уведомления', **TOKENS_PARAMETER))
@method_decorator(name='partial_update',
                  decorator=swagger_auto_schema(
                      tags=['notification'],
                      operation_description='Изменение уведомления', ))
@method_decorator(name='destroy',
                  decorator=swagger_auto_schema(
                      tags=['notification'],
                      operation_description='Удаление уведомления', ))
class NotificationViewSet(ModelViewSet):
    """CRUD Уведомления"""

    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateNotificationSerializer
        elif self.action == 'partial_update':
            return UpdateNotificationSerializer
        else:
            return NotificationSerializer
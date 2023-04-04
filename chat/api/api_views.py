from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from drf_yasg.utils import swagger_auto_schema
from task_manager.swagger_schema import TOKENS_PARAMETER
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from chat.models import Room
from chat.serializers import CreateRoomSerializer


@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      tags=['room'],
                      operation_description='Получение списка загруженных через реестр исполнителей',
                      **TOKENS_PARAMETER))
class CreateRoomViewSet(GenericViewSet, CreateModelMixin):
    """Создание чат-комнаты"""

    serializer_class = CreateRoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(
            name=f'chat {self.request.user.username}-support {datetime.utcnow()}',
            host=self.request.user
        )


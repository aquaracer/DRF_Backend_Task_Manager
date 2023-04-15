from datetime import datetime
from rest_framework import serializers

from .models import Room, Message
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """Пользователь"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "password",]
        extra_kwargs = {'password': {'write_only': True}}


class MessageSerializer(serializers.ModelSerializer):
    """Сообщение"""

    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Message
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj: Message):
        return obj.created.strftime("%d-%m-%Y %H:%M:%S")


class CreateRoomSerializer(serializers.ModelSerializer):
    """Создание чат-комнаты"""

    name = serializers.HiddenField(default=f'{datetime.utcnow()}')

    class Meta:
        model = Room
        fields = ["id", "name", ]
        read_only_fields = ("id",)


class RoomSerializer(serializers.ModelSerializer):
    """Отображение чат-комнаты"""

    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["pk", "name", "host", "messages", "current_users", "last_message",]
        depth = 1
        read_only_fields = ["messages", "last_message",]

    def get_last_message(self, obj: Room):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data

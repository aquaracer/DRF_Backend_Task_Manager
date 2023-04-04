from django.db import models
from common.models import AbstarctBaseModel


class Room(AbstarctBaseModel):
    """Комната"""

    name = models.CharField(max_length=255, unique=True)
    host = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name="rooms", blank=True, null=True)
    current_users = models.ManyToManyField('core.User', related_name="current_rooms", blank=True)

    def __str__(self):
        return f"Room({self.name} {self.host})"


class Message(AbstarctBaseModel):
    """Сообщение"""

    room = models.ForeignKey("chat.Room", on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(max_length=500)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        return f"Message({self.user} {self.room})"

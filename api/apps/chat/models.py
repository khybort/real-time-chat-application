from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.authentication.models import User
from apps.chat.domain.entities.message_entity import MessageEntity
from apps.chat.domain.entities.room_entity import RoomEntity
from apps.core.base_model import BaseModel


class Room(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, blank=True)
    
    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @staticmethod
    def from_entity(entity: RoomEntity):
        users = User.objects.filter(id__in=entity.members)
        room = Room(
            id=entity.id,
            name=entity.name,
            is_deleted=entity.is_deleted,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
        room.members.set(users)
        return room

    def to_entity(self) -> RoomEntity:
        return RoomEntity(
            id=self.id,
            name=self.name,
            members=[member.id for member in self.members.all()],
            is_deleted=self.is_deleted,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        


class Message(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default="general")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} in {self.room}: {self.content[:20]}"
    
    @staticmethod
    def from_entity(entity: MessageEntity):
        return Message(
            id=entity.id,
            room_id=entity.room_id,
            user_id=entity.user_id,
            content=entity.content,
            is_deleted=entity.is_deleted,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def to_entity(self) -> MessageEntity:
        return MessageEntity(
            id=self.id,
            room_id=self.room_id,
            user_id=self.user_id,
            content=self.content,
            is_deleted=self.is_deleted,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

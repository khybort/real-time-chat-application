from typing import List
from apps.authentication.domain.repositories.user_repository import UserRepository
from apps.authentication.models import User
from apps.chat.domain.entities.message_entity import MessageEntity
from apps.chat.domain.repositories.room_repository import RoomRepository
from apps.chat.domain.repositories.message_repository import MessageRepository
from apps.chat.models import Message, Room

class MessageRepositoryImpl(MessageRepository):
    def __init__(self, room_repository: RoomRepository , user_repository: UserRepository):
        self.room_repository= room_repository
        self.user_repository = user_repository
    
    def get(self, id_) -> MessageEntity:
        message_instance = Message.objects.get(id=id_)
        return message_instance.to_entity()

    
    def create_message(self, room_id: int, user_id: int, content: str) -> MessageEntity | None:
        message = Message.objects.create(
            user=User.from_entity(self.user_repository.get(user_id)),
            room=Room.from_entity(self.room_repository.get(room_id)),
            content=content
        )
        return message.to_entity() if message else None

    def get_messages(self, room_name: str, limit=50) -> List[MessageEntity]:
        room_entity = self.room_repository.get_room_by_name(name=room_name)
        messages = Message.objects.filter(room=Room.from_entity(room_entity)).order_by('created_at')[:limit]
        return [message.to_entity() for message in messages]
    
    def update_message(self, entity: MessageEntity, validated_data: dict) -> MessageEntity:
        message_instance = Message.objects.get(id=entity.id)
        message_instance.content = validated_data.get('content', message_instance.content)
        message_instance.save()
        return message_instance.to_entity()
    
    def delete_message(self, id: int) -> bool:
        message_instance = Message.objects.get(id=id)
        message_instance.is_deleted = True
        return True
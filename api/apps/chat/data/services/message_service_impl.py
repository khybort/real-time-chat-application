from typing import List
from apps.authentication.domain.repositories.user_repository import UserRepository
from apps.chat.domain.repositories.room_repository import RoomRepository
from apps.chat.domain.repositories.message_repository import MessageRepository
from apps.chat.domain.entities.message_entity import MessageEntity
from apps.chat.domain.services.message_service import MessageService


class MessageServiceImpl(MessageService):
    def __init__(self, message_repository: MessageRepository, room_repository: RoomRepository, user_repository: UserRepository):
        self.message_repository = message_repository
        self.room_repository = room_repository
        self.user_repository = user_repository
    
    def get_message(self, id_) -> MessageEntity:
        return self.message_repository.get(id_)
    
    def get_messages(self, room_name: str, limit=50) -> List[MessageEntity]:
        return self.message_repository.get_messages(room_name, limit)
    
    def create_message(self, room_id: int, user_id: int, content: str) -> MessageEntity:
        return self.message_repository.create_message(room_id, user_id, content)
    
    def update_message(self, entity: MessageEntity, validated_data: dict) -> MessageEntity:
        return self.message_repository.update_room(entity, validated_data)
    
    def delete_message(self, id: int)->bool:
        return self.message_repository.delete_room(id)
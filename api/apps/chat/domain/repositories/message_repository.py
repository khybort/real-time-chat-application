from abc import abstractmethod
from typing import List

from apps.authentication.domain.repositories.user_repository import UserRepository
from apps.chat.domain.repositories.room_repository import RoomRepository
from apps.chat.domain.entities.message_entity import MessageEntity
from apps.core.base_repository import BaseRepository


class MessageRepository(BaseRepository[MessageEntity]):
    def __init__(self, room_repository: RoomRepository, user_repository: UserRepository):
        self.room_repository = room_repository
        self.user_repository = user_repository
    @abstractmethod
    def create_message(self, room_id: int, user_id: int, content: str) -> MessageEntity | None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_messages(self, room_name: str, limit=50) -> List[MessageEntity]:
        raise NotImplementedError()
    
    @abstractmethod
    def update_message(self, entity: MessageEntity, validated_data: dict) -> MessageEntity:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_message(self, id: int) -> bool:
        raise NotImplementedError()
    
from typing import List
from apps.chat.domain.entities.message_entity import MessageEntity
from apps.core.base_service import BaseService


class MessageService(BaseService[MessageEntity]):
    def __init__(self, message_repository):
        self.message_repository = message_repository
    
    def get(self, id_) -> MessageEntity:
        raise NotImplementedError()
    
    def get_messages(self, room_name: str, limit=50) -> List[MessageEntity]:
        raise NotImplementedError()
    
    def create_message(self, room_id: int, user_id: int, content: str) -> MessageEntity:
        raise NotImplementedError()
    
    def update_message(self, entity: MessageEntity, validated_data: dict) -> MessageEntity:
        NotImplementedError()
        
    def delete_message(self, id: int) -> bool:
        raise NotImplementedError()

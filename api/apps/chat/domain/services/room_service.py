from abc import abstractmethod
from typing import List
from apps.chat.domain.entities.room_entity import RoomEntity
from apps.core.base_service import BaseService


class RoomService(BaseService[RoomEntity]):
    def __init__(self, room_repository):
        self.room_repository = room_repository
    
    @abstractmethod
    def get_rooms(self) -> List[RoomEntity]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_room_by_name(self, name: str) -> RoomEntity:
        raise NotImplementedError()
    
    def create_room(self, name: str) -> RoomEntity:
        raise NotImplementedError()
    
    def update_room(self, entity: RoomEntity, name: str) -> RoomEntity:
        NotImplementedError()
        
    def delete_room(self, id) -> bool:
        raise NotImplementedError()
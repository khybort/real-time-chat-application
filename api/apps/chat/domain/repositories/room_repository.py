from abc import abstractmethod
from apps.chat.domain.entities.room_entity import RoomEntity
from apps.core.base_repository import BaseRepository

class RoomRepository(BaseRepository[RoomEntity]):
    @abstractmethod
    def get_rooms(self) -> RoomEntity:
        raise NotImplementedError()
    
    @abstractmethod
    def get_room_by_name(self, name: str) -> RoomEntity:
        raise NotImplementedError()
    
    @abstractmethod
    def create_room(self, name: str) -> RoomEntity:
        raise NotImplementedError()
    
    @abstractmethod
    def update_room(self, entity: RoomEntity, name: str) -> RoomEntity:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_room(self, id: int) -> bool:
        raise NotImplementedError()

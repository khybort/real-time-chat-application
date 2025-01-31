from typing import List
from apps.chat.domain.repositories.room_repository import RoomRepository
from apps.chat.domain.services.room_service import RoomService
from apps.chat.domain.entities.room_entity import RoomEntity


class RoomServiceImpl(RoomService):
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository
    
    def get(self, id_: int) -> RoomEntity:
        return self.room_repository.get(id_)
    
    def get_rooms(self) -> List[RoomEntity]:
        return self.room_repository.get_rooms()
    
    def get_room_by_name(self, name: str) -> RoomEntity:
        return self.room_repository.get_room_by_name(name)
    
    def create_room(self, name: str) -> RoomEntity:
        return self.room_repository.create_room(name)
    
    def update_room(self, room: RoomEntity, name: str) -> RoomEntity:
        return self.room_repository.update_room(room, name)
    
    def delete_room(self, id: int) -> bool:
        return self.room_repository.delete_room(id)
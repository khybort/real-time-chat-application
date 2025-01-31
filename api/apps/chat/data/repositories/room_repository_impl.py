from typing import List
from apps.chat.domain.entities.room_entity import RoomEntity
from apps.chat.domain.repositories.room_repository import RoomRepository
from apps.chat.models import Room

class RoomRepositoryImpl(RoomRepository):
    def get(self, id_: int) -> RoomEntity:
        return Room.objects.get(id=id_).to_entity()
    
    def get_rooms(self) -> List[RoomEntity]:
        rooms = Room.objects.all()
        return [room.to_entity() for room in rooms]
    
    def get_room_by_name(self, name: str) -> RoomEntity:
        return Room.objects.get(name=name).to_entity()
    
    def create_room(self, name: str) -> RoomEntity:
        if Room.objects.filter(name=name).exists():
            raise ValueError("Room with the same name already exists.")
        room = Room.objects.create(name=name)
        return room.to_entity()

    def update_room(self, room: RoomEntity, name: str) -> RoomEntity:
        room_instance = Room.objects.get(id=room.id)
        room_instance.name = name
        return room_instance.to_entity()
    
    def delete_room(self, id: int) -> bool:
        room_instance = Room.objects.get(id=id)
        room_instance.is_deleted = True
        return True
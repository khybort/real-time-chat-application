from apps.shared.dependencies import get_room_service, get_user_service
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

class RoomViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self):
        self.room_service = get_room_service()
        self.user_service = get_user_service()

    def list(self, request):
        rooms = self.room_service.get_rooms()
        room_data = [
            {"id": room.id, "name": room.name, "created_at": room.created_at}
            for room in rooms
        ]
        return Response(room_data)

    def retrieve(self, request, pk=None):
        room = self.room_service.get(pk)
        if room:
            return Response({
                "id": room.id,
                "name": room.name,
                "created_at": room.created_at,
            })
        return Response({"detail": "Room not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        name = data.get("name")

        if not name:
            return Response({"detail": "Room name is required."}, status=status.HTTP_400_BAD_REQUEST)

        room = self.room_service.create_room(name)
        return Response({
            "id": room.id,
            "name": room.name,
            "created_at": room.created_at,
        }, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        room = self.room_service.get(pk)
        if not room:
            return Response({"detail": "Room not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        name = data.get("name", room.name)

        updated_room = self.room_service.update_room(room, name)
        return Response({
            "id": updated_room.id,
            "name": updated_room.name,
            "created_at": updated_room.created_at,
        })

    def destroy(self, request, pk=None):
        room = self.room_service.get(pk)
        if room:
            self.room_service.delete_room(room.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Room not found."}, status=status.HTTP_404_NOT_FOUND)

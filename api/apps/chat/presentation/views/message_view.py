from apps.shared.dependencies import get_message_service, get_room_service
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

class MessageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self):
        self.message_service = get_message_service()
        self.room_service = get_room_service()

    def list(self, request):
        room_name = request.query_params.get('room_name')
        if not room_name:
            return Response({"detail": "Room name is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        room = self.room_service.get_room_by_name(room_name)
        if not room:
            return Response({"detail": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        
        messages = self.message_service.get_messages(room_name)
        message_data = [
            {
                "id": msg.id,
                "user_id": msg.user_id,
                "room_id": msg.room_id,
                "content": msg.content,
                "created_at": msg.created_at,
            }
            for msg in messages
        ]
        return Response(message_data)

    def retrieve(self, request, pk=None):
        message = self.message_service.get(pk)
        if message:
            return Response({
                "id": message.id,
                "user_id": message.user_id,
                "room_id": message.room_id,
                "content": message.content,
                "created_at": message.created_at,
            })
        return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        user_id = data.get("user_id")
        room_id = data.get("room_id")
        content = data.get("content")

        if not all([user_id, room_id, content]):
            return Response({"detail": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        message = self.message_service.create_message(user_id=user_id, room_id=room_id, content=content)
        return Response({
            "id": message.id,
            "user_id": message.user_id,
            "room_id": message.room_id,
            "content": message.content,
            "created_at": message.created_at,
        }, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        message = self.message_service.get(pk)
        if not message:
            return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        content = data.get("content", message.content)

        updated_message = self.message_service.update_message(message, {"content": content})
        return Response({
            "id": updated_message.id,
            "user_id": updated_message.user_id,
            "room_id": updated_message.room_id,
            "content": updated_message.content,
            "created_at": updated_message.created_at,
        })

    def destroy(self, request, pk=None):
        message = self.message_service.get(pk)
        if message:
            self.message_service.delete_message(message.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

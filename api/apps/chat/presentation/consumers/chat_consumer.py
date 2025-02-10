import json

from apps.chat.presentation.consumers.base_consumer import BaseConsumer
from asgiref.sync import sync_to_async
from apps.shared.dependencies import get_room_service


class ChatConsumer(BaseConsumer):
    async def connect(self):
        await super().connect()
        self.room_service = get_room_service()
        self.group_name = f"chat_{self.room_name}"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        if not text_data:
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        if data.get('type') == 'join_room':
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
        elif data.get('type') == 'typing':
            if data.get('sender') != self.scope['user'].username:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'user_typing',
                        'sender': data['sender']
                    }
                )
        elif data.get('type') == 'stop_typing':
            if data.get('sender') != self.scope['user'].username:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'user_stop_typing',
                        'sender': data['sender']
                    }
                )
        elif data.get('type') == 'chat_message':
            if 'message' not in data or 'sender' not in data:
                await self.send(text_data=json.dumps({
                    'error': 'Message field or sender is missing',
                }))
                return

            message = data['message']
            sender = data['sender']
            
            try:
                room = await sync_to_async(self.room_service.get_room_by_name)(self.room_name)
                user = await sync_to_async(self.user_service.get_user_by_username)(username=sender)
                await sync_to_async(self.message_service.create_message)(room_id=room.id, user_id=user.id, content=message)
                
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender': sender,
                        'room_name': self.room_name
                    }
                )
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'error': str(e),
                }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'room_name': event['room_name']
        }))

    async def user_typing(self, event):
        if event['sender'] != self.scope['user'].username:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'sender': event['sender']
            }))

    async def user_stop_typing(self, event):
        if event['sender'] != self.scope['user'].username:
            await self.send(text_data=json.dumps({
                'type': 'stop_typing',
                'sender': event['sender']
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

import json

from apps.chat.presentation.consumers.base_consumer import BaseConsumer
from asgiref.sync import sync_to_async
from apps.shared.dependencies import get_room_service


class ChatConsumer(BaseConsumer):
    async def connect(self):
        await super().connect()
        self.group_name = f"chat_{self.room_name}"
        self.room_service = get_room_service()
        
        user = await self.validate_token(self.token)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        self.user = user
        await self.accept()

    async def receive(self, text_data):
        if not text_data:
            await self.send(text_data=json.dumps({
                'error': 'Empty content received',
            }))
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format',
            }))
            return

        if 'content' not in data:
            await self.send(text_data=json.dumps({
                'error': 'Message field is missing',
            }))
            return

        content = data['content']
        sender = data['sender']
        room = await sync_to_async(self.room_service.get_room_by_name)(self.room_name)
        user = await sync_to_async(self.user_service.get_user_by_username)(username=sender)
        new_message = await sync_to_async(self.message_service.create_message)(room_id=room.id, user_id=user.id, content=content)
        await self.channel_layer.group_send(
            group=self.group_name,
            message={
                'type': 'chat_message',
                'content': new_message.content,
                'sender': sender,
                'room_name': self.room_name
            }
        )

    async def chat_message(self, event):
        content = event['content']
        sender = event['sender']
        room_name = event['room_name']

        await self.send(text_data=json.dumps({
            'content': content,
            'sender': sender,
            'room_name': room_name
        }))

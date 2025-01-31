import json
from apps.chat.presentation.consumers.base_consumer import BaseConsumer
from asgiref.sync import sync_to_async

class ChatHistoryConsumer(BaseConsumer):
    async def connect(self):
        await super().connect()
        self.group_name = f'chat_history_{self.room_name}'
        await self.channel_layer.group_add(
            group=self.group_name,
            channel=self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        messages = await sync_to_async(self.message_service.get_messages)(room_name=self.room_name)
        message_list = []
        for msg in messages:
           sender = await sync_to_async(self.user_service.get)(id_=msg.user_id) 
           message_list.append( {
                'content': msg.content,
                'sender': sender.username,
                'room_name': self.room_name,
            })
           
        await self.send(text_data=json.dumps({
            'type': 'chat_history',
            'messages': message_list
        }))

import urllib
from apps.shared.dependencies import get_message_service, get_user_service
from channels.generic.websocket import AsyncWebsocketConsumer
import jwt
from asgiref.sync import sync_to_async

class BaseConsumer(AsyncWebsocketConsumer):
    async def validate_token(self, token):
        from rest_framework_simplejwt.tokens import AccessToken
        if not token:
            await self.close()
            return
        try:
            access_token = AccessToken(token)
            username = access_token['username']
        except jwt.ExpiredSignatureError:
            await self.close()
            return
        except jwt.DecodeError:
            await self.close()
            return
        
        user = await sync_to_async(self.user_service.get_user_by_username)(username)
        
        if not user:
            await self.close()
            return
        
        return user
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.token = urllib.parse.parse_qs(self.scope['query_string'].decode('utf-8')).get('token', [None])[0]
        self.user_service = get_user_service()
        self.message_service = get_message_service()
        self.user = await self.validate_token(self.token)
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass
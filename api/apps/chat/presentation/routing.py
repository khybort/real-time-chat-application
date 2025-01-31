from django.urls import re_path
from .consumers.chat_consumer import ChatConsumer
from .consumers.chat_history_consumer import ChatHistoryConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/history/(?P<room_name>\w+)/$', ChatHistoryConsumer.as_asgi()),
]

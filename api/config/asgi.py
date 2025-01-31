import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chat.presentation.routing import websocket_urlpatterns
from decouple import config

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    config("DJANGO_SETTINGS_MODULE", "config.settings"),
)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})

from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlspatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)$", ChatConsumer.as_asgi())
]

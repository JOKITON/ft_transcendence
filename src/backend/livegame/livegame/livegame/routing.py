from django.urls import re_path
from .consumers import GameConsumer

websocket_urlspatterns = [
    re_path(r"^ws/game/(?P<room_name>[^/]+)$", GameConsumer.as_asgi()),
]

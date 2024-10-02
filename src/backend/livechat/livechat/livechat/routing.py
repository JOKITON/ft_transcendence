from django.urls import re_path
from .consumers import ConsumerLiveChat

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ConsumerLiveChat.as_asgi()),
]

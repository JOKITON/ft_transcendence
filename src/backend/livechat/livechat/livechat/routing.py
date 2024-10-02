from .consumers import ConsumerLiveChat
from django.urls import re_path

websocket_urlpatterns = [
    re_path(
        r"api/v1/livechat/ws/chat/(?P<room_name>\w+)/$", ConsumerLiveChat.as_asgi()
    ),
]

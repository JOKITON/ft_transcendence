from django.urls import path
from .views import ListRoomView, CreateRoomView, DeleteRoomView, CreateChatView

urls_patterns = [
    path("create/chat", CreateRoomView.as_view()),
    path("create/room", CreateChatView.as_view()),
    path("delete", DeleteRoomView.as_view()),
    path("rooms", ListRoomView.as_view()),
]

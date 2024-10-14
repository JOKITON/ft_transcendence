from .views import ListRoomView, CreateRoomView, DeleteRoomView, CreateChatView
from django.urls import path

urls_patterns = [
    path("create/room", CreateRoomView.as_view()),
    #    path("create/chat", CreateChatView.as_view()),
    #    path("delete", DeleteRoomView.as_view()),
    #    path("rooms", ListRoomView.as_view()),
]

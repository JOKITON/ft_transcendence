from django.urls import path
from .views import ListRoomView, CreateRoomView, DeleteRoomView

urls_patterns = [
    path("create", CreateRoomView.as_view()),
    path("delete", DeleteRoomView.as_view()),
    path("rooms", ListRoomView.as_view()),
]

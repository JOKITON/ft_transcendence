from django.urls import path
from .views import allUsers

urlpatterns = [
    path("users", allUsers.as_view(), name="users"),
]

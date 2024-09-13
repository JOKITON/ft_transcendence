from django.urls import path
from .views import AllUsers, InviteFriendView

urlpatterns = [
    path("users", AllUsers.as_view(), name="users"),
    path("invite", InviteFriendView.as_view(), name="invite"),
]

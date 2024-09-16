from .views import AllUsers, InviteFriendView, InviteStatusView, DeleteFriendView
from django.urls import path

urlpatterns = [
    path("users", AllUsers.as_view(), name="users"),
    path("add", InviteFriendView.as_view(), name="invite"),
    path("edit", InviteStatusView.as_view(), name="edit"),
    path("del", DeleteFriendView.as_view(), name="del"),
    path("block", DeleteFriendView.as_view(), name="block"),  # Todo:
    path("unblock", DeleteFriendView.as_view(), name="unblock"),  # Todo:
    path("friends", DeleteFriendView.as_view(), name="friends"),  # Todo:
]

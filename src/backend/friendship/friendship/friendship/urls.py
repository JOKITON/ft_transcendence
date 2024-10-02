from .views import (
    AllUsers,
    InviteFriendView,
    InviteStatusView,
    DeleteFriendView,
    PendingFriendRequestsView,
    AcceptFriendRequestView,
    GetFriendsView,
    RejectFriendRequestView,
    BlockUserView,
    UnlockUserView
)
from django.urls import path

urlpatterns = [
    path("users", AllUsers.as_view(), name="users"),
    path("add", InviteFriendView.as_view(), name="invite"),
    path("pendingReq", PendingFriendRequestsView.as_view(), name="pendingReq"),
    path("edit", InviteStatusView.as_view(), name="edit"),
    path("del", DeleteFriendView.as_view(), name="del"),
    path("friends", GetFriendsView.as_view(), name="friends"),
    path("acceptFriendReq", AcceptFriendRequestView.as_view(),
         name="acceptFriendReq"),
    path("rejectFriendReq", RejectFriendRequestView.as_view(),
         name="rejectFriendReq"),
    path("blockFriend", BlockUserView.as_view(), name="blockFriend"),
    path("unblockFriend", UnlockUserView.as_view(), name="unblockFriend"),
]


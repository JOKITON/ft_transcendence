from .views import AllUsers, InviteFriendView, InviteStatusView
from django.urls import path

urlpatterns = [
    path("users", AllUsers.as_view(), name="users"),
    path("add", InviteFriendView.as_view(), name="invite"),
    path("edit", InviteStatusView.as_view(), name="edit"),
]

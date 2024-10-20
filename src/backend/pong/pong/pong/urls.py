from django.urls import path
from .views import (
    CreateDefaultPlayerView,
    TournamentAIView,
    Tournament2PView,
    Tournament4P,
    Tournament8P,
)
from .views_get import (
    TournamentListView,
    LeaderBoardView,
    UserDataView,
)

urlpatterns = [
    path("ai", TournamentAIView.as_view(), name="post-ai"),
    path("2p", Tournament2PView.as_view(), name="post-2p"),
    path("4p", Tournament4P.as_view(), name="post-4p"),
    path("8p", Tournament8P.as_view(), name="post-8p"),
    
    path("register/<int:pk>/", CreateDefaultPlayerView.as_view(), name="get-user"),
    path("user/<int:pk>/", UserDataView.as_view(), name="get-user"),
    path("leaderboard", LeaderBoardView.as_view(), name="get-leaderboard"),
    path("data", TournamentListView.as_view(), name="get-results"),
]

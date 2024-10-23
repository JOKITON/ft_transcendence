from django.urls import path
from .views import (
    CreateDefaultPlayerView,
    PostGameView,
    PostGameStateView,
    Tournament4P,
    Tournament8P,
)
from .views_get import (
    TournamentListView,
    LeaderBoardView,
    UserDataView,
    AnyPongGameDataView,
    PongGameDataView,
)

urlpatterns = [
    # Get/Post game state
    path("get-state/<int:pk>/", PongGameDataView.as_view(), name="get-state"),
    path("get-state/<str:tournament_type>/<int:pk>/", AnyPongGameDataView.as_view(), name="get-state"),
    path("post-state", PostGameStateView.as_view(), name="post-ai-state"),
    
    # Store complete game data
    path("ai", PostGameView.as_view(), name="post-ai"),
    path("2p", PostGameView.as_view(), name="post-2p"),
    path("4p", Tournament4P.as_view(), name="post-4p"),
    path("8p", Tournament8P.as_view(), name="post-8p"),
    
    # Create initial table for User
    path("register/<int:pk>/", CreateDefaultPlayerView.as_view(), name="get-user"),
    # Get all data from Users/PongGames
    path("user/<int:pk>/", UserDataView.as_view(), name="get-user"),
    path("leaderboard", LeaderBoardView.as_view(), name="get-leaderboard"),
    path("data", TournamentListView.as_view(), name="get-results"),
]

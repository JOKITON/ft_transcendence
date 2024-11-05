from django.urls import path
from .views import (
    CreateDefaultPlayerView,
    PostGameView,
    PostGameStateView,
    Tournament4PStateView,
    Tournament4PView,
    Tournament8P,
    health_check,
)
from .views_get import (
    TournamentListView,
    LeaderBoardView,
    UserDataView,
    AnyPongGameDataView,
    Pong2PGameDataView,
    PongGameDataView,
)

urlpatterns = [
    path("health", health_check, name="health"),
    
    # Get/Post game state
    path("get-state/<int:pk>/", PongGameDataView.as_view(), name="get-state"),
    path("get-state/<str:tournament_type>/<int:id1>/", AnyPongGameDataView.as_view(), name="get-state"),
    path("get-state/<str:tournament_type>/<int:id1>/<int:id2>/", Pong2PGameDataView.as_view(), name="get-state"),
    path("post-state", PostGameStateView.as_view(), name="post-ai/2p-state"),
    path("4p/post-state", Tournament4PStateView.as_view(), name="post-4p-state"),
    
    # Store complete game data
    path("ai", PostGameView.as_view(), name="post-ai"),
    path("2p", PostGameView.as_view(), name="post-2p"),
    path("4p", Tournament4PView.as_view(), name="post-4p"),
    path("8p", Tournament8P.as_view(), name="post-8p"),
    
    # Create initial table for User
    path("register/<int:pk>/", CreateDefaultPlayerView.as_view(), name="get-user"),
    # Get all data from Users/PongGames
    path("user/<int:pk>/", UserDataView.as_view(), name="get-user"),
    path("leaderboard", LeaderBoardView.as_view(), name="get-leaderboard"),
    path("data", TournamentListView.as_view(), name="get-results"),
]

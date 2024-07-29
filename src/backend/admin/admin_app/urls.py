from django.urls import path
from .views import PlayerListCreateAPIView, GameSessionListCreateAPIView, ScoreListCreateAPIView

urlpatterns = [
    path('api/players/', PlayerListCreateAPIView.as_view(), name='player-list-create'),
    path('api/gamesessions/', GameSessionListCreateAPIView.as_view(), name='gamesession-list-create'),
    path('api/scores/', ScoreListCreateAPIView.as_view(), name='score-list-create'),
]

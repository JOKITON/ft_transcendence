# shared_models/urls.py
from django.urls import path
from .views import PlayerListCreateAPIView, GameSessionListCreateAPIView, ScoreListCreateAPIView

urlpatterns = [
    path('players/', PlayerListCreateAPIView.as_view(), name='player-list-create'),
    path('gamesessions/', GameSessionListCreateAPIView.as_view(), name='gamesession-list-create'),
    path('scores/', ScoreListCreateAPIView.as_view(), name='score-list-create'),
]

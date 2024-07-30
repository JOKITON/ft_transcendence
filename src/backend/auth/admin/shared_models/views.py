# shared_models/views.py
from rest_framework import generics
from .models import Player, GameSession, Score
from .serializers import PlayerSerializer, GameSessionSerializer, ScoreSerializer

class PlayerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class GameSessionListCreateAPIView(generics.ListCreateAPIView):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer

class ScoreListCreateAPIView(generics.ListCreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

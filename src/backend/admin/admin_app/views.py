# admin_app/views.py
from rest_framework import generics
from .models import Player, GameSession, Score
from .serializers import PlayerSerializer, GameSessionSerializer, ScoreSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import BasePermission

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser

class PlayerListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsSuperuser]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class GameSessionListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsSuperuser]
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer

class ScoreListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsSuperuser]
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    
class UserListView(generics.ListCreateAPIView):
    permission_classes = [IsSuperuser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperuser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

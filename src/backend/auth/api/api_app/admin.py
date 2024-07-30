from django.contrib import admin
from .models import Player, GameSession, Score

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2', 'start_time', 'end_time')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('game_session', 'player', 'points')

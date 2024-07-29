from django.contrib import admin
from .models import Player, GameSession, Score

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'date_joined')  # Changed 'username' to 'user' and added 'email'
    search_fields = ('user__username', 'user__email')  # Access fields on User model
    
    def email(self, obj):
        return obj.user.email
    email.admin_order_field = 'user__email'
    email.short_description = 'Email'

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2', 'start_time', 'end_time')
    search_fields = ('player1__username', 'player2__username')
    list_filter = ('start_time', 'end_time')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('game_session', 'player', 'points')
    search_fields = ('game_session__id', 'player__username')
    list_filter = ('game_session', 'player')

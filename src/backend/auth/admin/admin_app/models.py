# admin_app/models.py
from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class GameSession(models.Model):
    player1 = models.ForeignKey(Player, related_name='player1_games', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='player2_games', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.player1} vs {self.player2} ({self.start_time} - {self.end_time})"

class Score(models.Model):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.player} scored {self.points} in game {self.game_session}"

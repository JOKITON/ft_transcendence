# shared_models/models.py
from django.db import models

class Player(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class GameSession(models.Model):
    player1 = models.ForeignKey(Player, related_name='player1_sessions', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='player2_sessions', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Session between {self.player1} and {self.player2}"

class Score(models.Model):
    game_session = models.ForeignKey(GameSession, related_name='scores', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='scores', on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.player} scored {self.points} points in session {self.game_session}"

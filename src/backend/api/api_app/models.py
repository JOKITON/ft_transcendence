from django.db import models

class Player(models.Model):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class GameSession(models.Model):
    player1 = models.ForeignKey(Player, related_name='player1_sessions', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='player2_sessions', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Game between {self.player1} and {self.player2} on {self.start_time}"

class Score(models.Model):
    game_session = models.ForeignKey(GameSession, related_name='scores', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.player} scored {self.points} points in game {self.game_session.id}"

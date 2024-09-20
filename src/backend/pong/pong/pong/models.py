from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tournament(models.Model):
    tournament_type_choices = [
        ('AI', 'AI Tournament'), ('2P', '2P Tournament')
    ]

    winner = models.CharField(max_length=100)
    player1 = models.CharField(max_length=100)
    player2 = models.CharField(max_length=100)
    score_player1 = models.IntegerField()
    score_player2 = models.IntegerField()
    tournament_type = models.CharField(max_length=2, choices=tournament_type_choices, default='2P')

    def __str__(self):
        return f"{self.tournament_type} - {self.winner}"

# 8 Player Tournament

class Player(models.Model):
    name = models.CharField(max_length=255)
    score = models.JSONField()
    position = models.IntegerField()

    def __str__(self):
        return f"{self.name} (Position: {self.position}, Score: {self.score})"

class FinalRound(models.Model):
    player_one = models.CharField(max_length=255)
    player_two = models.CharField(max_length=255)
    winner = models.CharField(max_length=255)
    loser = models.CharField(max_length=255)

    def __str__(self):
        return f"Final Round: {self.winner.name} vs {self.loser.name}"

class SemiFinal(models.Model):
    semi_one = models.CharField(max_length=255)
    semi_two = models.CharField(max_length=255)
    semi_three = models.CharField(max_length=255)
    semi_four = models.CharField(max_length=255)

    def __str__(self):
        return "Semi Final Round"

class Tournament8P(models.Model):
    players = models.ManyToManyField(Player)
    final_round = models.OneToOneField(FinalRound, on_delete=models.CASCADE)
    semi_finals = models.OneToOneField(SemiFinal, on_delete=models.CASCADE)
    tournament_type = models.CharField(max_length=3, default='8P')

    def __str__(self):
        return f"Tournament {self.tournament_type} with {self.players.count()} players"

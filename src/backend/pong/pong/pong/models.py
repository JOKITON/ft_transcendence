from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Player(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    position = models.IntegerField(blank=True)

    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    total_games = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} (Position: {self.position}, Score: {self.score})"

class PongGame(models.Model):
    tournament_type_choices = [
        ('AI', 'AI Tournament'), ('2P', '2P Tournament')
    ]

    tournament_type = models.CharField(max_length=2, choices=tournament_type_choices, default='2P')
    winner = models.CharField(max_length=255)
    id_player1 = models.ForeignKey(Player, on_delete=models.DO_NOTHING, related_name='player1_data', null=True, blank=True)
    id_player2 = models.ForeignKey(Player, on_delete=models.DO_NOTHING,  related_name='player2_data', null=True, blank=True)
    name_player1 = models.CharField(max_length=255, null=True, blank=True)
    name_player2 = models.CharField(max_length=255, null=True, blank=True)
    score_player1 = models.IntegerField()
    score_player2 = models.IntegerField()

    def __str__(self):
        return f"{self.tournament_type} - {self.winner}"

# 8 Player Tournament
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

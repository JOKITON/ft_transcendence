from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()

class Player(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    total_games = models.IntegerField(default=0)
    total_score = models.FloatField(default=0)
    time_played = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    # Tournament related fields
    scores = models.JSONField(default=list)  # Assuming scores are stored as a list of integers
    last_position = models.IntegerField(default=0)
    avg_position = models.IntegerField(default=0)

    class Meta:
        db_table = 'pong_player'
    
    def __str__(self):
        return f"{self.name} (Position: {self.avg_position}, Avg Score: {self.avg_score})"
    
    @property
    def avg_score(self):
        if self.total_games > 0:
            return round(float(self.total_score) / self.total_games, 2)
        return 0

class PongGame(models.Model):
    tournament_type_choices = [
        ('AI', 'AI Game'),
        ('2P', '2 Player'),
        ('4P', '4 Player'),
        ('8P', '8 Player'),
    ]
    
    status_choices = [
        ('P', 'Pending'),
        ('C', 'Completed'),
    ]

    status = models.CharField(max_length=1, choices=status_choices, default='P')
    tournament_type = models.CharField(max_length=2, choices=tournament_type_choices, default='2P')
    winner = models.CharField(max_length=255)
    player1 = models.ForeignKey(Player, on_delete=models.DO_NOTHING, related_name='player1_data', null=True, blank=True)
    player2 = models.ForeignKey(Player, on_delete=models.DO_NOTHING,  related_name='player2_data', null=True, blank=True)
    player_ids = models.JSONField(null=True, blank=True)
    player_names = models.JSONField(null=True, blank=True)
    player_scores = models.JSONField(null=True, blank=True)
    time_played = models.IntegerField(default=0)
    player_hits = models.JSONField(null=True, blank=True)

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

class Tournament4P(models.Model):
    status_choices = [
        ('P', 'Pending'),
        ('C', 'Completed'),
    ]

    status = models.CharField(max_length=1, choices=status_choices, default='P')
    players = models.ManyToManyField(Player)
    final_round = models.OneToOneField(FinalRound, on_delete=models.CASCADE)
    tournament_type = models.CharField(max_length=3, default='4P')

    def __str__(self):
        return f"Tournament {self.tournament_type} with {self.players.count()} players"


class Tournament8P(models.Model):
    status_choices = [
        ('P', 'Pending'),
        ('C', 'Completed'),
    ]

    status = models.CharField(max_length=1, choices=status_choices, default='P')
    players = models.ManyToManyField(Player)
    final_round = models.OneToOneField(FinalRound, on_delete=models.CASCADE)
    semi_finals = models.OneToOneField(SemiFinal, on_delete=models.CASCADE)
    tournament_type = models.CharField(max_length=3, default='8P')

    def __str__(self):
        return f"Tournament {self.tournament_type} with {self.players.count()} players"

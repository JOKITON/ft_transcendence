from django.db import models


class round(models.Model):
    player1 = models.CharField(max_length=255)
    player2 = models.CharField(max_length=255)
    score1 = models.IntegerField()
    score2 = models.IntegerField()

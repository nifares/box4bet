from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BetfairSession(models.Model):
    session_token = models.CharField(max_length=500)
    active = models.BooleanField(default=False)

class CompetitionKind(models.Model):
    name = models.CharField(max_length=100)

class Competition(models.Model):
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=False)
    kind = models.ForeignKey(CompetitionKind, on_delete=models.CASCADE)
    free_entry = models.BooleanField(default=True)
    entry_fee = models.IntegerField(default=None)

class Match(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    home_score = models.IntegerField()
    home_score_90 = models.IntegerField()
    away_score = models.IntegerField()
    away_score_90 = models.IntegerField()
    locked = models.BooleanField(default=False)

class Odd(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    value = models.FloatField()
    winner = models.BooleanField(default=False)
    name = models.CharField(max_length=100)

class Score(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
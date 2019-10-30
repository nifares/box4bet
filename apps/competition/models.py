from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.contrib.auth.models import User

# Create your models here.

class BetfairSession(models.Model):
    session_token = models.CharField(max_length=500)
    active = models.BooleanField(default=False)

class CompetitionKind(models.Model):
    name = models.CharField(max_length=100)
    betfair_id = models.BigIntegerField()
    enabled = models.BooleanField(default=False)

class Competition(models.Model):
    name = models.CharField(max_length=100)
    kind = models.ForeignKey(CompetitionKind, on_delete=models.CASCADE)
    region = models.CharField(max_length=100, default='UNK')
    entry_fee = models.IntegerField(null=True)
    fee_currency = models.CharField(max_length=3, default='CBL')
    betfair_id = models.BigIntegerField(unique=True)
    enabled = models.BooleanField(default=False)

class Event(models.Model):
    name = models.CharField(max_length=100)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    home = models.CharField(max_length=100)
    away = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    home_score = models.IntegerField(null=True)
    home_score_90 = models.IntegerField(null=True)
    away_score = models.IntegerField(null=True)
    away_score_90 = models.IntegerField(null=True)
    locked = models.BooleanField(default=False)
    live = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    betfair_id = models.BigIntegerField(unique=True)

class Odd(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    prize = models.FloatField(null=True)
    winner = models.BooleanField(default=False)
    betfair_id = models.BigIntegerField()
    betfair_name = models.CharField(max_length=100)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['event', 'betfair_id'], name='unique_betfair_id_event')
        ]

class Score(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
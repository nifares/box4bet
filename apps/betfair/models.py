from django.db import models


class BetfairSession(models.Model):
    session_token = models.CharField(max_length=500)
    active = models.BooleanField(default=False)
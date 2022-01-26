from django.db import models

from .game import Game


class Event(models.Model):

    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    date = models.DateField()
from django.db import models

from levelupapi.models.gamer import Gamer

from .game import Game


class Event(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    date = models.DateField()
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    
    
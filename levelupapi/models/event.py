from django.db import models

from levelupapi.models.gamer import Gamer

from .game import Game


class Event(models.Model):

    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    
    
from django.db import models

from levelupapi.models.gamer import Gamer

class Game(models.Model):

    name = models.CharField(max_length=15)
    description = models.CharField(max_length=50)
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
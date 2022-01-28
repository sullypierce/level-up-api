from django.db import models

from levelupapi.models.gamer import Gamer
from .gametype import Gametype

class Game(models.Model):

    name = models.CharField(max_length=15)
    description = models.CharField(max_length=50)
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    maker = models.CharField(max_length=50)
    skill_level = models.CharField(max_length=50)
    gametype = models.ForeignKey(Gametype, on_delete=models.CASCADE)
    
    @property
    def event_count(self):
        return self.__event_count

    @event_count.setter
    def event_count(self, value):
        self.__event_count = value
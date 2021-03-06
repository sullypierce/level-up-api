from django.db import models

from levelupapi.models.gamer import Gamer

from .game import Game


class Event(models.Model):

    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='events')
    date = models.DateField()
    time = models.TimeField()
    
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
    
    @property
    def registration_count(self):
        return self.__registration_count

    @registration_count.setter
    def registration_count(self, value):
        self.__registration_count = value
    
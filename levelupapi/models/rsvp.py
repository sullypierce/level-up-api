from .event import Event
from .gamer import Gamer
from django.db import models


class Rsvp(models.Model):

    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
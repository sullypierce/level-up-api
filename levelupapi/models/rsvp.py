from .event import Event
from .gamer import Gamer
from django.db import models


class Rsvp(models.Model):

    gamer_id = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
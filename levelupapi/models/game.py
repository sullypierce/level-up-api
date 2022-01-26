from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):

    name = models.CharField(max_length=15)
    description = models.CharField(max_length=50)
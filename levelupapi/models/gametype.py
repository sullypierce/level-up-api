from django.db import models



class Gametype(models.Model):
    
    label = models.CharField(max_length=50)
from django.db import models
from datetime import datetime

# Create your models here.
class Player(models.Model):
    objects = models.Manager()

    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    primaryPosition = models.CharField(max_length=200)
    alternatePositions = models.CharField(max_length=200)
    currentTeam = models.CharField(max_length=200)

    created_at = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return 'Name: %s %s (%s)' % (self.firstName, self.lastName, self.primaryPosition)

class Game(models.Model):
    objects = models.Manager()

    #home team info
    homeTeam = models.CharField(max_length=40)
    homeTeamScore = models.IntegerField(default=0) 

    #away team info
    awayTeam = models.CharField(max_length=40)
    awayTeamScore = models.IntegerField(default=0)

    #game info
    week = models.IntegerField(default=0)
    eid = models.IntegerField(default=0)
    def __str__(self):
        return '%s: %s - %s: %s' % (self.homeTeam, self.homeTeamScore, self.awayTeam, self.awayTeamScore)
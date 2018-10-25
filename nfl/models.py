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

    #abbreviated name
    shortName = models.CharField(default="J. Doe", max_length=100)

    #id provided by nfl
    nfl_id = models.CharField(default="00-000000", max_length=50)

    created_at = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return 'Name(id): %s (%s)' % (self.shortName, self.nfl_id)

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

class Game_Offense_Stats(models.Model):
    objects = models.Manager()

    game_eid = models.IntegerField(default=0)
    player_nfl_id = models.CharField(max_length=50)

    #Passing Stats
    pass_attempts = models.IntegerField(default=0)
    pass_completions = models.IntegerField(default=0)
    pass_yards = models.IntegerField(default=0)
    pass_tds = models.IntegerField(default=0)
    pass_ints = models.IntegerField(default=0)

    #Rushing Stats
    rush_attempts = models.IntegerField(default=0)
    rush_yards = models.IntegerField(default=0)
    rush_tds = models.IntegerField(default=0)

    #Receiving Stats
    receptions = models.IntegerField(default=0)
    rec_yards = models.IntegerField(default=0)
    rec_tds = models.IntegerField(default=0)

    def __str__(self):
        return '%s: Pass yds: %s - Rush yds: %s - Rec yds: %s' % (self.player_nfl_id, self.pass_yards, self.rush_yards, self.rec_yards)

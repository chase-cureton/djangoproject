from nfl.models import Player,Game
import requests
import json

def get_players(limit=None, **filters):
    if limit:
        return Player.objects.filter(**filters)[:limit]
    return Player.objects.filter(**filters)

def import_games():
    URL = "http://www.nfl.com/liveupdate/scorestrip/ss.json"

    r = requests.get(url = URL)
    gameJSON = json.loads(r.text)

    for game in gameJSON['gms']:
        print ('%s (Home): %s - %s (Away): %s' % (
            game['hnn'], game['hs'], game['vnn'], game['vs']
        ))

        #dbGame = Game.objects.all().filter(homeTeam=game['hnn'], week=gameJSON['w'])
        dbGame = Game.objects.get(homeTeam=game['hnn'], week=gameJSON['w'])

        print (dbGame)

        if dbGame:
            print('Game already exists(%s)' % (dbGame))
            dbGame.eid = "%s" % game['eid']
            dbGame.homeTeamScore = "%s" % game['hs']
            dbGame.awayTeamScore = "%s" % game['vs']
            dbGame.save()
        else:
            print('Week: %s' % gameJSON['w'])
            dbGame = Game(homeTeam=game['hnn'], awayTeam=game['vnn'],
                          homeTeamScore="%s" % game['hs'], awayTeamScore="%s" % game['vs'],
                          week="%s" % gameJSON['w'], eid="%s" % game['eid'])
            dbGame.save()

            dbGame = Game.objects.all().filter(homeTeam=game['hnn'], week=gameJSON['w'])
            print('Saved game to db(%s)' % (dbGame))
from nfl.models import Player,Game,Game_Offense_Stats
import requests
import json
import xml.etree.ElementTree as ET

def get_players(limit=None, **filters):
    if limit:
        return Player.objects.filter(**filters)[:limit]
    return Player.objects.filter(**filters)

def import_past_games(season, season_type, week=0, current_week=1):
    URL = "http://www.nfl.com/ajax/scorestrip?season=%s&seasonType=%s&week=%s" % (season, season_type, week)

    r = requests.get(allow_redirects=False, url=URL)
    gameXML = ET.fromstring(r.text)

    for child in gameXML:
        print (child.tag, child.attribute)


def import_current_games():
    #URL = "http://www.nfl.com/liveupdate/scorestrip/ss.json"
    URL = "http://www.nfl.com/liveupdate/scorestrip?season=201818&seasonType=REG&week=7/ss.json"

    r = requests.get(allow_redirects=False, url = URL)
    gameJSON = json.loads(r.text)

    for game in gameJSON['gms']:
        print ('%s (Home): %s - %s (Away): %s' % (
            game['hnn'], game['hs'], game['vnn'], game['vs']
        ))

        dbGame = Game.objects.all().filter(homeTeam=game['hnn'], week=gameJSON['w'])
        #dbGame = Game.objects.get(homeTeam=game['hnn'], week=gameJSON['w'])

        if dbGame:
            print('Game already exists(%s)' % (dbGame))
            dbGame = Game.objects.get(homeTeam=game['hnn'], week=gameJSON['w'])
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

        
        dbGame = Game.objects.get(homeTeam=game['hnn'], week=gameJSON['w'])
        print('Saved game to db(%s)' % (dbGame))
    
        print (dbGame)
        import_game_details(dbGame)


def import_game_details(dbGame):
    URL = "http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json" % (dbGame.eid, dbGame.eid)
    #URL = "http://www.nfl.com/liveupdate/game-center/2018102101/2018102101_gtd.json"

    print ('URL: %s' % URL)

    r = requests.get(url = URL)
    gameDetailsJSON = json.loads(r.text)

    #print (gameDetailsJSON)

    # passing stats (Home)
    upsert_passing_stats(gameDetailsJSON, dbGame, 'home')
    upsert_passing_stats(gameDetailsJSON, dbGame, 'away')

def upsert_passing_stats(gameDetailsJSON, dbGame, location):
    for nfl_id in gameDetailsJSON['%s' % dbGame.eid][location]['stats']['passing']:
        passing_stats = gameDetailsJSON['%s' % dbGame.eid][location]['stats']['passing']['%s' % nfl_id]

        print ('Passing Stats: %s' % passing_stats)

        dbPlayer = Player.objects.all().filter(nfl_id=nfl_id)

        if dbPlayer:
            dbPlayer = Player.objects.get(nfl_id=nfl_id)
            dbPlayer.currentTeam = dbGame.homeTeam
            dbPlayer.shortName = passing_stats['name']
        else:
            dbPlayer = Player(shortName=passing_stats['name'], nfl_id=nfl_id)
            dbPlayer.save()

        offense_stats = Game_Offense_Stats.objects.all().filter(player_nfl_id=dbPlayer.nfl_id, game_eid=dbGame.eid)

        if offense_stats:
            offense_stats = Game_Offense_Stats.objects.get(player_nfl_id=dbPlayer.nfl_id, game_eid=dbGame.eid)
            offense_stats.pass_attempts = passing_stats['att']
            offense_stats.pass_completions = passing_stats['cmp']
            offense_stats.pass_yards = passing_stats['yds']
            offense_stats.pass_tds = passing_stats['tds']
            offense_stats.pass_ints = passing_stats['ints']
        else:
            offense_stats = Game_Offense_Stats(player_nfl_id=dbPlayer.nfl_id, game_eid=dbGame.eid, 
                                               pass_attempts=passing_stats['att'],
                                               pass_completions=passing_stats['cmp'], pass_yards=passing_stats['yds'],
                                               pass_tds=passing_stats['tds'], pass_ints=passing_stats['ints'])
            offense_stats.save()

        print (offense_stats)

def print_player_stats():
    dbPlayers = Player.objects.all()
    dbGameStats = Game_Offense_Stats.objects.all()

    for dbPlayer in dbPlayers:
        player_stats = dbGameStats.get(player_nfl_id=dbPlayer.nfl_id)
        print ('%s - Pass Yards: %s' % (dbPlayer.shortName, player_stats.pass_yards))
from nfl.models import Player,Game,Game_Offense_Stats
import requests
import json
import xml.etree.ElementTree as ET

def get_players(limit=None, **filters):
    if limit:
        return Player.objects.filter(**filters)[:limit]
    return Player.objects.filter(**filters)

def ImportPastGames(season=2018, season_type='REG', week=0, current_week=8):

    while week < current_week:
        URL = "http://www.nfl.com/ajax/scorestrip?season=%s&seasonType=%s&week=%s" % (season, season_type, week)

        week = week + 1
        ImportPastGames(week=week)
        ImportGamesForWeek(URL)

def ImportGamesForWeek(URL):
    r = requests.get(allow_redirects=False, url=URL)
    gameXML = ET.fromstring(r.text)

    for games in gameXML:
        print ('Tag: %s - Attrib: %s' % (games.tag, games.attrib))

        week = games.get('w')

        for game in games.findall('g'):
            print ('Tag: %s - Attrib: %s' % (game.tag, game.attrib))

            eid = game.get('eid')
            home_team = game.get('hnn')
            home_team_score = game.get('hs')
            away_team = game.get('vnn')
            away_team_score = game.get('vs')

            dbGame = Game.objects.all().filter(eid=eid)

            if dbGame:
                print('Do nothing, already exists')
            else:
                game = Game(eid=eid, week=week,
                            homeTeam=home_team, homeTeamScore=home_team_score,
                            awayTeam=away_team, awayTeamScore=away_team_score)
                game.save()
            
            dbGame = Game.objects.get(eid=eid)
            ImportGameDetails(dbGame)

def ImportCurrentGames():
    URL = "http://www.nfl.com/liveupdate/scorestrip/ss.json"
    #URL = "http://www.nfl.com/liveupdate/scorestrip?season=201818&seasonType=REG&week=7/ss.json"

    r = requests.get(allow_redirects=False, url = URL)
    gameJSON = json.loads(r.text)

    for game in gameJSON['gms']:
        print ('%s (Home): %s - %s (Away): %s' % (
            game['hnn'], game['hs'], game['vnn'], game['vs']
        ))

        dbGame = Game.objects.all().filter(eid=game['eid'])
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
        ImportGameDetails(dbGame)

def ImportGameDetails(dbGame):
    URL = "http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json" % (dbGame.eid, dbGame.eid)
    #URL = "http://www.nfl.com/liveupdate/game-center/2018102101/2018102101_gtd.json"

    print ('URL: %s' % URL)
    r = requests.get(url = URL)

    print ('Request Status: %s' % r.status_code)

    if (r.status_code == 200):
        gameDetailsJSON = json.loads(r.text)

        # passing stats
        UpsertPassingStats(gameDetailsJSON, dbGame, 'home')
        UpsertPassingStats(gameDetailsJSON, dbGame, 'away')

        # rushing stats
        UpsertRushingStats(gameDetailsJSON, dbGame, 'home')
        UpsertRushingStats(gameDetailsJSON, dbGame, 'away')

        # receiving stats
        UpsertReceivingStats(gameDetailsJSON, dbGame, 'home')
        UpsertReceivingStats(gameDetailsJSON, dbGame, 'away')
    else:
        print ('Game(%s) has not started' % dbGame.eid)

def UpsertPassingStats(gameDetailsJSON, dbGame, location):
    for nfl_id in gameDetailsJSON['%s' % dbGame.eid][location]['stats']['passing']:
        passing_stats = gameDetailsJSON['%s' % dbGame.eid][location]['stats']['passing']['%s' % nfl_id]

        print ('Passing Stats: %s' % passing_stats)

        dbPlayer = UpsertPlayer(nfl_id, location, dbGame, passing_stats)

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

def UpsertRushingStats(gameDetailsJSON, dbGame, location):
    for nfl_id in gameDetailsJSON['%s' % dbGame.eid][location]['stats']['rushing']:
        rushing_stats = gameDetailsJSON['%s' % dbGame.eid][location]['stats']['rushing']['%s' % nfl_id]

        #print ('Rushing Stats: %s' % rushing_stats)

        dbPlayer = UpsertPlayer(nfl_id, location, dbGame, rushing_stats)

        offense_stats = Game_Offense_Stats.objects.all().filter(player_nfl_id=dbPlayer.nfl_id, game_eid=dbGame.eid)

        if offense_stats:
            offense_stats = Game_Offense_Stats.objects.get(player_nfl_id=dbPlayer.nfl_id, game_eid=dbGame.eid)
            offense_stats.rush_attempts = rushing_stats['att']
            offense_stats.rush_yards = rushing_stats['yds']
            offense_stats.rush_tds = rushing_stats['tds']
            offense_stats.longest_rush = rushing_stats['lng']
            offense_stats.longest_rush_td = rushing_stats['lngtd']
        else:
            offense_stats = Game_Offense_Stats(player_nfl_id=dbPlayer.nfl_id, game_eid=dbGame.eid, 
                                               rush_attempts=rushing_stats['att'],
                                               rush_yards=rushing_stats['yds'], rush_tds=rushing_stats['tds'],
                                               longest_rush=rushing_stats['lng'], longest_rush_td=rushing_stats['lngtd'])
            offense_stats.save()

        #print (offense_stats)

def UpsertReceivingStats(gameDetailsJSON, dbGame, location):
    for nfl_id in gameDetailsJSON['%s' % dbGame.eid][location]['stats']['receiving']:
        receiving_stats = gameDetailsJSON['%s' % dbGame.eid][location]['stats']['receiving']['%s' % nfl_id]

        #print ('Receiving Stats: %s' % receiving_stats)

        dbPlayer = UpsertPlayer(nfl_id, location, dbGame, receiving_stats)

        offense_stats = Game_Offense_Stats.objects.all().filter(player_nfl_id=dbPlayer.nfl_id, game_eid=dbGame.eid)

        if offense_stats:
            offense_stats = Game_Offense_Stats.objects.get(player_nfl_id=dbPlayer.nfl_id, game_eid=dbGame.eid)
            offense_stats.rec_yards = receiving_stats['yds']
            offense_stats.rec_tds = receiving_stats['tds']
            offense_stats.longest_rec = receiving_stats['lng']
            offense_stats.longest_rec_td = receiving_stats['lngtd']
        else:
            offense_stats = Game_Offense_Stats(player_nfl_id=dbPlayer.nfl_id, game_eid=dbGame.eid, 
                                               rec_yards=receiving_stats['yds'], rec_tds=receiving_stats['tds'],
                                               longest_rec=receiving_stats['lng'], longest_rec_td=receiving_stats['lngtd'])
            offense_stats.save()

        #print (offense_stats)

def UpsertPlayer(nfl_id, location, dbGame, stats):
    dbPlayer = Player.objects.all().filter(nfl_id=nfl_id)

    if dbPlayer:
        dbPlayer = Player.objects.get(nfl_id=nfl_id)
        dbPlayer.currentTeam = dbGame.homeTeam if location == "home" else dbGame.awayTeam
        dbPlayer.shortName = stats['name']
        dbPlayer.save()
    else:
        dbPlayer = Player(shortName=stats['name'], nfl_id=nfl_id,
                          currentTeam=dbGame.homeTeam if location == "home" else dbGame.awayTeam)
        dbPlayer.save()

    return dbPlayer

def PrintPlayerStats():
    dbPlayers = Player.objects.all()
    dbGameStats = Game_Offense_Stats.objects.all()

    for dbPlayer in dbPlayers:
        player_stats = dbGameStats.get(player_nfl_id=dbPlayer.nfl_id)
        print ('%s - Pass Yards: %s' % (dbPlayer.shortName, player_stats.pass_yards))
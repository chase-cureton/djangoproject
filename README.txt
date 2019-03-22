Fantasy Football Helper Application
- This is the start of a web application that will be able to import player stats in real-time and store in a hosted db.
- A front facing website would allow users to query player statistics as a single visit users. Users who create an account will be able
- to create player watchlists and certain criteria to receive notifications on player stat changes & eventually player news releases.

To run (currently):
1.) cd to project folder
2.) docker-compose build
3.) docker-compose up -d

To import player stats (currently):
1.) shell into djangoproject_web container
2.) python manage.py shell
3.) from nfl.Service import nfl_service
4.) nfl_service.ImportPastGames()
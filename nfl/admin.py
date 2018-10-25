from django.contrib import admin

# Register your models here.
from .models import Player, Game, Game_Offense_Stats

admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Game_Offense_Stats)

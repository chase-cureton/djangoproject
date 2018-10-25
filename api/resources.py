# api/resources.py

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from posts.models import Posts
from nfl.models import Player, Game

class PostResource(ModelResource):
    class Meta:
        queryset = Posts.objects.all()
        resource_name = 'post'
        authorization = Authorization()

class PlayerResource(ModelResource):
    class Meta:
        queryset = Player.objects.all()
        resource_name = 'player'
        authorization = Authorization()

class GameResource(ModelResource):
    class Meta:
        queryset = Game.objects.all()
        resource_name = 'game'
        authorization = Authorization()
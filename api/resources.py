# api/resources.py

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from posts.models import Posts
from nfl.models import Player

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
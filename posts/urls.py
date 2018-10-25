from django.conf.urls import url, include
from api.resources import PostResource, PlayerResource, GameResource
from . import views

post_resource = PostResource()
player_resource = PlayerResource()
game_resource = GameResource()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
    url(r'^create/$', views.create, name='create'),
    url(r'^api/', include(post_resource.urls)),
    #url(r'^api/', include(player_resource.urls)),
    #url(r'^api/', include(game_resource.urls)),
]
from django.conf.urls import url, include
from api.resources import PlayerResource, GameResource
from . import views

player_resource = PlayerResource()
game_resource = GameResource()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/', include(player_resource.urls)),
    url(r'^api/', include(game_resource.urls)),
]
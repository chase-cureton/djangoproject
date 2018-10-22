from django.conf.urls import url, include
from api.resources import PlayerResource
from . import views

player_resource = PlayerResource()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/', include(player_resource.urls))
]
from django.conf.urls import url, include
from api.resources import PostResource
from . import views

post_resource = PostResource()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
    url(r'^create/$', views.create, name='create'),
    url(r'^api/', include(post_resource.urls))
]
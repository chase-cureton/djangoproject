# api/resources.py

from tastypie.resources import ModelResource
from posts.models import Posts

class PostResource(ModelResource):
    class Meta:
        queryset = Posts.objects.all()
        resource_name = 'posts'
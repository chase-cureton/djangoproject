from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Player

# Create your views here.
def index(request):
    #return HttpResponse('HELLO FROM POSTS')

    players = Player.objects.all()[:10]

    context = {
        'title' : 'Latest Posts',
        'players': players
    }

    return render(request, 'posts/index.html', context)
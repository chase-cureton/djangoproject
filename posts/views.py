from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Posts
from .forms import CreatePostForm

# Create your views here.
def index(request):
    #return HttpResponse('HELLO FROM POSTS')

    posts = Posts.objects.all()[:10]

    context = {
        'title' : 'Latest Posts',
        'posts': posts
    }

    return render(request, 'posts/index.html', context)

def details(request, id):
    post = Posts.objects.get(id=id)

    context = {
        'post': post
    }

    return render(request, 'posts/details.html', context)

def create(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)

        if form.is_valid():
            #Save to db
            post_title = form.cleaned_data['post_title']
            post_body = form.cleaned_data['post_body']
            
            Posts.objects.create(title=post_title, body=post_body)
            return HttpResponseRedirect('/posts/')

    else :
        form = CreatePostForm()
        context = {
            'title' : 'Create a Post',
            'form' : form
        }

        return render(request, 'posts/create.html', context)
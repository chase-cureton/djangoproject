from django import forms
from django.db import models
from .models import Posts

class CreatePostForm(forms.Form):
    #objects = models.Manager()
    post_title = forms.CharField(label='Title', max_length=200)
    post_body = forms.CharField(label='Content', widget=forms.Textarea(attrs={ 'required' : True,
                                                                               'class' : 'materialize-textarea' }))
    post_attachment = forms.FileField(allow_empty_file=True)

    def save(self):
        print ('File "%s" would presumably be saved to disk now.' % self.post_attachment)

        new_post = Posts(title=self.post_title, body=self.post_body)
        new_post.save()
        pass

    class Meta:
        verbose_name_plural = "Forms"
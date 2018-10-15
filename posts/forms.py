from django import forms
from django.db import models

class CreatePostForm(forms.Form):
    #objects = models.Manager()

    post_title = forms.CharField(label='Title', max_length=200)
    post_body = forms.CharField(widget=forms.Textarea(attrs={ 'required' : True,
                                                              'class' : 'materialize-textarea' }))
    class Meta:
        verbose_name_plural = "Forms"
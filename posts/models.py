from django.db import models
from datetime import datetime

# Create your models here.
class Posts(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=200)
    body = models.TextField()
    attachment_path = models.URLField(default="https://google.com")
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return 'Title: %s' % (self.title)
    class Meta:
        verbose_name_plural = "Posts"
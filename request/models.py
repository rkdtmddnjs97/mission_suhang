from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Hashtag(models.Model):
    name = models.CharField(max_length=50)

class Post(models.Model):
    title=models.CharField(max_length=200)
    writer = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published')
    body = models.TextField()
    user = models.ManyToManyField(User, blank=True)
    hashtag = models.ManyToManyField(Hashtag)

    def __str__(self):
        return self.title

class Comment(models.Model):
    writer = models.CharField(max_length=200)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
# Create your models here.

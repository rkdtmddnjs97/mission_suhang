from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
# Create your models here.
class Hashtag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=200,null=True)
    writer = models.CharField(max_length=200,null=True)
    pub_date = models.DateTimeField('Date published',null=True)
    body = models.TextField(null=True)
    user = models.ManyToManyField(User, blank=True)
    status=models.CharField(default='ready',max_length=200)
    hashtag = models.ManyToManyField(Hashtag, related_name="tag")
 
   
    def __str__(self):
        return self.title

class ApplyMission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    applier=models.ForeignKey(User, on_delete=models.CASCADE,related_name='applier',null=True)
    



class Comment(models.Model):
    writer = models.CharField(max_length=200)
    content = models.TextField(null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
# Create your models here.
class Opinion(models.Model):
    o_writer = models.CharField(max_length=200)
    o_content = models.TextField(null=True)
    o_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
from django.db import models
from django.contrib.auth.models import User
from hashtag.models import Hashtag

# Create your models here.


class Post(models.Model):
    title=models.CharField(max_length=200,null=True)
    writer = models.CharField(max_length=200,null=True)
    pub_date = models.DateTimeField('Date published',null=True)
    body = models.TextField(null=True)
    user = models.ManyToManyField(User, blank=True)
    status=models.CharField(default='ready',max_length=200)
    hashtag = models.ManyToManyField(Hashtag, related_name="post_tag")
    approved_id=models.CharField(null=True,max_length=200)
    s_flag=models.BooleanField(default=False)
    attached_img=models.ImageField(upload_to='attached_img/', null=True, blank=True)
    

    def __str__(self):
        return self.title

class ApplyMission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    applier=models.ForeignKey(User, on_delete=models.CASCADE,related_name='applier',null=True)
    
class submit_form(models.Model):
    title=models.CharField(max_length=200,null=True)
    writer = models.CharField(max_length=200,null=True)
    pub_date = models.DateTimeField('Date published',null=True)
    body = models.TextField(null=True)
    submit=models.OneToOneField(Post,on_delete=models.CASCADE, null=True)

class Comment(models.Model):
    writer = models.CharField(max_length=200)
    content = models.TextField(null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
# Create your models here.
class Opinion(models.Model):
    writer = models.CharField(max_length=200)
    content = models.TextField(null=True)
    o_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
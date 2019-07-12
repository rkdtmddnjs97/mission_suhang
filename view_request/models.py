from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title=models.CharField(max_length=100)
    pub_date=models.DateTimeField('date published')
    body=models.TextField()
    def __str__(self):
        return self.title
        
    def summary(self):
        return self.body[:100] #100글자까지만 출력해라

class Comment(models.Model):
    writer = models.CharField(max_length=200,null=True)
    content = models.TextField(null=True)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE,null=True)
# Create your models here.

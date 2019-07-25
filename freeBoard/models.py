from django.db import models
from django.contrib.auth.models import User
from hashtag.models import Hashtag
# Create your models here.
class B_Blog(models.Model):
    title=models.CharField(max_length=200)
    writer=models.CharField(max_length=200)
    body=models.TextField()
    pub_date = models.DateTimeField('Date published',null=True)
    user = models.ManyToManyField(User, blank=True,related_name='user')
    hashtag = models.ManyToManyField(Hashtag, related_name="freeboard_tag")
    

    @property
    def total_likes(self):
        return self.user.count() #likes 컬럼의 값의 갯수를 센다

class B_Comment(models.Model):
    writer = models.CharField(max_length=200)
    content = models.TextField()
    post = models.ForeignKey(B_Blog, on_delete=models.CASCADE)
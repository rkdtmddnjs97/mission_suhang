from django.db import models
from django.contrib.auth.models import User
from hashtag.models import Hashtag
from django_fields import DefaultStaticImageField
# Create your models here.
class B_Blog(models.Model):
    title=models.CharField(max_length=200)
    writer=models.CharField(max_length=200)
    body=models.TextField()
    pub_date = models.DateTimeField('Date published',null=True)
    user = models.ManyToManyField(User, blank=True, related_name='user')
    dislike=models.ManyToManyField(User, blank=True,related_name='dislike')
    hashtag = models.ManyToManyField(Hashtag, related_name="freeboard_tag")
    attached_img=DefaultStaticImageField(upload_to='attached_img/', blank=True, default_image_path='images/default_free_img.png')
    attached_file=DefaultStaticImageField(upload_to='attached_file/', blank=True, default_image_path='files/dummy.txt')
    

    @property
    def total_likes(self):
        return self.user.count() #likes 컬럼의 값의 갯수를 센다
    @property
    def total_dislikes(self):
        return self.dislike.count() #likes 컬럼의 값의 갯수를 센다    

class B_Comment(models.Model):
    writer = models.CharField(max_length=200)
    content = models.TextField()
    post = models.ForeignKey(B_Blog, on_delete=models.CASCADE)
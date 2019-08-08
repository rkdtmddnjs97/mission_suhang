from django.db import models
from django_fields import DefaultStaticImageField
# Create your models here.

class Announcement(models.Model):
    title=models.CharField(max_length=200,null=True)
    writer=models.CharField(max_length=200, null=True)
    content=models.TextField(null=True)
    announcement_img=DefaultStaticImageField(upload_to='announcement_img/', blank=True, default_image_path='images/default_announcement_img.png')
    announcement_file=DefaultStaticImageField(upload_to='announcement_file/', blank=True, default_image_path='files/dummy.txt')
    
    pub_date = models.DateTimeField('Date published',null=True)


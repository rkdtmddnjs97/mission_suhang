from django.db import models

class Announcement(models.Model):
    title=models.CharField(max_length=200,null=True)
    writer=models.CharField(max_length=200, null=True)
    content=models.TextField(null=True)
    announcement_img=models.ImageField(upload_to='announcement_img/', null=True, blank=True)
    announcement_file=models.FileField(upload_to='announcement_file/', null=True, blank=True)
    pub_date = models.DateTimeField('Date published',null=True)
# Create your models here.

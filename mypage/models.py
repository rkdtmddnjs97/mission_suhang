from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from request.models import Post



class MTM_chat(models.Model):
        profile_fk=models.ForeignKey(Profile,on_delete=models.CASCADE, null=True,related_name='profile_fk')
        request_fk=models.ForeignKey(Profile,on_delete=models.CASCADE, null=True,related_name='request_fk')

class chatting(models.Model):
    chatting_fk=models.ForeignKey(MTM_chat,on_delete=models.CASCADE, null=True)
    writer = models.CharField(max_length=200)
    content = models.TextField(null=True)
    
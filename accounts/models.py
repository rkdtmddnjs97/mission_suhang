from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class accountInfo(models.Model):
    university=models.CharField(max_length=200,null=True)
    department=models.CharField(max_length=200,null=True)
    name=models.CharField(max_length=200,null=True)
    nickname=models.CharField(max_length=200,null=True)
    introduction=models.TextField(null=True)
    Fin = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
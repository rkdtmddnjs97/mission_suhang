from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    university=models.CharField(max_length=200,null=True)
    department=models.CharField(max_length=200,null=True)
    name=models.CharField(max_length=200,null=True)
    nickname=models.CharField(max_length=200,null=True)
    introduction=models.TextField(null=True)

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from hashtag.models import Hashtag



# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    university=models.CharField(max_length=200,null=True)
    department=models.CharField(max_length=200,null=True)
    name=models.CharField(max_length=200,null=True)
    hashtag=models.ManyToManyField(Hashtag, related_name="my_tag")
    introduction=models.TextField(null=True)
    email=models.CharField(max_length=200,null=True)
    approval=models.BooleanField(default=False)
    ssn=models.CharField(max_length=200,null=True)
    profile_id=models.CharField(unique=True,max_length=200,null=True)
    profile_img=models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    money=models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


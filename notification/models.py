from django.db import models
from accounts.models import Profile
# Create your models here.
class Notification(models.Model):

    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('mission_application', 'Mission_application')
    )

    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='creator')
    to = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='to')

    notifi_comment = models.TextField(null=True, blank=True)

    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
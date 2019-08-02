from django.db import models
from accounts.models import Profile
from request.models import Post
# Create your models here.
class Notification(models.Model):

    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('mission_apply', 'Mission_apply'),
        ('mission_accept', 'Mission_accept'),
        ('mission_reject', 'Mission_reject'),
        ('mision_submit', 'Mission_submit'),
        ('mission_complete', 'Mission_complete'),
        ('chat', 'Chat')
    )

    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='creator')
    to = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='to')

    notifi_comment = models.TextField(null=True, blank=True)
    notifi_post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='notifi_post')

    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
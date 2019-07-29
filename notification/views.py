from django.shortcuts import render
from .models import Notification
from django.contrib.auth.models import User
# Create your views here.

def get(request):
    user = request.user.profile

    notifications = Notification.objects.filter(to=user)
    
    return render(request, 'notifications.html', {'notifications':notifications})

def create_notification(creator, to, notification_type, comment=None):
    notification = Notification.objects.create(
        creator=creator,
        to=to,
        notification_type=notification_type,
        notifi_comment=comment
    )
    notification.save()
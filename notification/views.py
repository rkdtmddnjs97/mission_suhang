from django.shortcuts import render, redirect
from .models import Notification
from django.contrib.auth.models import User
# Create your views here.

def notifications(request):
    user = request.user.profile
    notifications = Notification.objects.filter(to=user)
    for noti in notifications:
        noti.confirmation = True
        noti.save()
    return render(request, 'notifications.html', {'notifications':notifications})

def confirm_notification(request, noti_id):
    notification = Notification.objects.get(id=noti_id)
    notification.confirmation = True

    return {}

def create_notification(creator, to, notification_type, comment=None, post_id=None):
    if creator != to:
        notification = Notification.objects.create(
            creator=creator,
            to=to,
            notification_type=notification_type,
            notifi_comment=comment,
            notifi_post_id=post_id
        )
        notification.save()

def delete_notification(request, notification_id):
    del_notifi = Notification.objects.get(id=notification_id)
    del_notifi.delete()
    return redirect('notifications')
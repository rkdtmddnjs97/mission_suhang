from accounts.models import Profile
from notification.models import Notification
from django.contrib.auth.models import User

def add_variable_to_context(request):

    if request.user.is_anonymous:
        return {}
    elif request.user.is_superuser:
        superuser = request.user
        if superuser.profile.profile_id != 'admin':
            superuser.profile.profile_id = 'admin'
            superuser.profile.save()
        admin = Profile.objects.get(profile_id='admin')
        notifications = Notification.objects.filter(to=admin, confirmation=False)
        notifi_count = notifications.count()
        return {'notification_list': notifications, 'notifi_count':notifi_count}
    else:
        # if Profile.objects.get(profile_id=request.user.username).exist:
        user = Profile.objects.get(profile_id=request.user.username)
        notifications = Notification.objects.filter(to=user, confirmation=False)
        notifi_count = notifications.count()
        return {'notification_list': notifications, 'notifi_count':notifi_count}


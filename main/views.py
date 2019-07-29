from django.shortcuts import render
from request.models import Post
from accounts.models import Profile
from notification.models import Notification
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    completed_posts = Post.objects.filter(status='completed')
    mission_completed = completed_posts.count()
    recent_posts=[]
    posts=Post.objects.order_by('-pub_date')
    for index,post in enumerate(posts):
        if index != 5:
             if post.status == 'ready':
                recent_posts.append(post)
    hot_users=[]
    profiles=Profile.objects.order_by('-mission_count')
    for index,profile in enumerate(profiles):
        if index != 5:
            if profile.mission_count != 0:
                 hot_users.append(profile)

    # user = Profile.objects.get(profile_id=request.user.username)
    # notifi = Notification.objects.filter(to=user)
    # count = notifi.count() 

    

    return render(request, 'home.html',{'recent_posts':recent_posts,'hot_users':hot_users, 'mission_completed':mission_completed})

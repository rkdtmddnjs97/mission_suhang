from django.shortcuts import render,redirect
from request.models import Post
from accounts.models import Profile
from notification.models import Notification
from django.contrib.auth.models import User
from mypage.models import complaint

# Create your views here.
def home(request):
    judge=False
    if request.user.is_superuser == True:
        judge=True
    print(judge)
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
    ready_number=0
    running_number=0
    for index,post in enumerate(posts):
        
        if post.status == 'ready':
            ready_number+=1
        elif post.status =='running':
            running_number+=1
    

    return render(request, 'home.html',{'recent_posts':recent_posts,'hot_users':hot_users, 'mission_completed':mission_completed,'ready_number':ready_number,'running_number':running_number,'judge':judge})

def dissatisfication(request):
    complaints=complaint.objects.all()
    return render(request,'complaint_board.html',{'complaints':complaints})

def requisition(request,complaint_id):
    tmp=complaint.objects.get(id=complaint_id)
    tmp.delete()
    return redirect('dissatisfication')
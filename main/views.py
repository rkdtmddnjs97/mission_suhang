from django.shortcuts import render,redirect
from request.models import Post
from accounts.models import Profile
from notification.models import Notification
from django.contrib.auth.models import User
from mypage.models import complaint
from .models import Announcement
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from hashtag.models import Hashtag

# Create your views here.
def home(request):
    judge=False
    if request.user.is_superuser == True:
        judge=True
    
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
                
    ready_number=0
    running_number=0
    for index,post in enumerate(posts):
        if post.status == 'ready':
            ready_number+=1
        elif post.status =='running':
            running_number+=1
            
    if request.user.is_anonymous or request.user.is_superuser:
        return render(request, 'home.html',{'recent_posts':recent_posts,'hot_users':hot_users, 'mission_completed':mission_completed,'ready_number':ready_number,'running_number':running_number, 'judge':judge })
    else:
        recommend_post = recommend_request(request)
        recommend_post_list = list(recommend_post)

        return render(request, 'home.html',{'recent_posts':recent_posts,'hot_users':hot_users, 'mission_completed':mission_completed,'ready_number':ready_number,'running_number':running_number, 'judge':judge, 'recommend_post':recommend_post, 'recommend_post_list':recommend_post_list})

def recommend_request(request):
    my_profile = Profile.objects.get(profile_id=request.user.username)
    my_hashtag = Hashtag.objects.filter(my_tag=my_profile)

    recommend_post = {}
    
    for tag in my_hashtag:
        tmp_post = []
        posts = Post.objects.filter(hashtag=tag)
        for post in posts:
            tmp_post.append(post)
        recommend_post[tag] = tmp_post

    return recommend_post

def dissatisfication(request):
    complaints=complaint.objects.all()
    return render(request,'complaint_board.html',{'complaints':complaints})

def requisition(request,complaint_id):
    tmp=complaint.objects.get(id=complaint_id)
    tmp.delete()
    return redirect('dissatisfication')

def announcement_board(request):
    announcements=Announcement.objects.all()
    judge=False
    if request.user.is_superuser == True:
        judge=True
    return render(request,'announcementBoard.html',{'announcements':announcements,'judge':judge})

def new_announcement(request):
    return render(request,'new_announcement.html')

def create_announcement(request):
    announcement=Announcement()
    announcement.title=request.POST['title']
    announcement.writer=request.user.username
    announcement.content=request.POST['body']
    announcement.pub_date=timezone.datetime.now()
    announcement.announcement_img = request.FILES.get('attached_img')
    announcement.announcement_file=request.FILES.get('attached_file')
    announcement.save()
    return redirect('announcement_board')
    
def announcement_detail(request,announcement_id):
    announcement=Announcement.objects.get(id=announcement_id)
    judge=False
    if request.user.is_superuser == True:
        judge=True
    return render(request,'announcement_detail.html',{'announcement':announcement,'judge':judge})

def announce_delete(request,announcement_id):
    announcement=Announcement.objects.get(id=announcement_id)
    announcement.delete()
    return redirect('announcement_board')

def announce_edit(request,announcement_id):
    announcement=Announcement.objects.get(id=announcement_id)
    return render(request,'announcement_edit.html',{'announcement':announcement})
    
def update_announce(request,announcement_id):
    announcement=Announcement.objects.get(id=announcement_id)
    announcement.title=request.POST['title']
    announcement.content=request.POST['body']

    if request.FILES.get('attached_img') is None:
        pass
    else:
        announcement.announcement_img = request.FILES.get('attached_img')
    if request.FILES.get('attached_file') is None: 
        pass
    else:
        announcement.announcement_file=request.FILES.get('attached_file')

    announcement.save()
    return redirect('announcement_detail',announcement_id)

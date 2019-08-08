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
from freeBoard.models import B_Blog
import operator

# Create your views here.
def home(request):
    judge=False
    if request.user.is_superuser == True:
        judge=True
    
    completed_posts = Post.objects.filter(status='completed')
    mission_completed = completed_posts.count()
    recent_posts=[]
    posts=Post.objects.order_by('-pub_date')

    #연관 검색에 사용할 의뢰게시판 데이터
    search_request_post = Post.objects.filter(status='ready')
    all_request_title = []
    for post_title in search_request_post:
        all_request_title.append(post_title.title)
    #자유게시판 데이터
    search_free_post = B_Blog.objects.all()
    all_free_title = []
    for post_title in search_free_post:
        all_free_title.append(post_title.title)

    for index,post in enumerate(posts):
        if index < 5:
             if post.status == 'ready':
                recent_posts.append(post)
    hot_users=[]
    profiles=Profile.objects.order_by('-mission_count')

    for index,profile in enumerate(profiles):
        if index < 5:
            if profile.mission_count != 0:
                 hot_users.append(profile)
    recent_announcements=[]
    tmp_announcements=Announcement.objects.order_by('-pub_date') 

    for index,tmp_announcement in enumerate(tmp_announcements):
        if index < 5:
            recent_announcements.append(tmp_announcement)
    recent_freeboard=[]      
    tmp_freeboards = B_Blog.objects.order_by('-pub_date')  

    for index,tmp_freeboard in enumerate(tmp_freeboards):
        if index < 5:
            recent_freeboard.append(tmp_freeboard)
                  
    ready_number=0
    running_number=0

    for index,post in enumerate(posts):
        if post.status == 'ready':
            ready_number+=1
        elif post.status =='running':
            running_number+=1
# 인기 게시판
    like_list={}
    for post in B_Blog.objects.all():
        like_list[post] = post.user.count()
    data= sorted(like_list.items(), key=operator.itemgetter(1), reverse = True)
    data = data[0:3]
    like_lists =[]
    for dat in data:
        like_lists.append(list(dat))
    # hot 의뢰 글
    scrap_list={}
    for post in Post.objects.all():
       if post.status != 'running' and post.status != 'completed':
            scrap_list[post] = post.user.count()
    datas= sorted(scrap_list.items(), key=operator.itemgetter(1), reverse = True)
    datas = datas[0:3]
    scrap_lists =[]
    for datt in datas:
           scrap_lists.append(list(datt))  
    
    if request.user.is_anonymous or request.user.is_superuser:
        return render(request, 'home.html',{'recent_posts':recent_posts,'hot_users':hot_users, 'mission_completed':mission_completed,'ready_number':ready_number,'running_number':running_number, 'judge':judge,'recent_announcements':recent_announcements, 'recent_freeboard': recent_freeboard, 'all_request_title':all_request_title, 'all_free_title':all_free_title, 'scrap_lists': scrap_lists , 'like_lists':like_lists})
    else:
        recommend_post = recommend_request(request)
        recommend_post_list = list(recommend_post)

        return render(request, 'home.html',{'recent_posts':recent_posts,'hot_users':hot_users, 'mission_completed':mission_completed,'ready_number':ready_number,'running_number':running_number, 'judge':judge, 'recommend_post':recommend_post, 'recommend_post_list':recommend_post_list,'recent_announcements':recent_announcements, 'recent_freeboard': recent_freeboard, 'all_request_title':all_request_title, 'all_free_title':all_free_title, 'scrap_lists': scrap_lists , 'like_lists':like_lists})

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

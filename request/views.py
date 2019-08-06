from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment,ApplyMission
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from accounts.models import Profile
from hashtag.models import Hashtag
from mypage.models import MTM_chat,chatting,Review
from notification.views import create_notification
from django.core.exceptions import ObjectDoesNotExist
from notification.views import create_notification
from django.utils.datastructures import MultiValueDictKeyError



def request_home(request):
    post_list=[]
    tmp= Post.objects.all()
    page = request.GET.get('page')
    for n in tmp:
        if n.status != 'completed' and n.status != 'running':
            post_list.append(n)
    
    if request.user.is_authenticated:
        my_scrap_post = Post.objects.filter(user = request.user)
        
        
    else:
        my_scrap_post = None
    post_list.reverse()
    paginator = Paginator(post_list, 3)
    total_len = len(post_list)
    try:
       post_list = paginator.get_page(page)
    except PageNotAnInterger:
       post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages) 
    index = post_list.number -1
    max_index = len(paginator.page_range)
    start_index = index -2 if index >= 2 else 0
    if index <2:
        end_index = 5 - start_index
    else:
        end_index = index+3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])

    return render(request, 'request_home.html', {'blogs':post_list,'scrap_post':my_scrap_post, 'page_range':page_range, 'total_len':total_len,'max_index':max_index-2})
                                        

def detail(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post = post_id)
    page = request.GET.get('page')
    reversed_comment=[]
    for comment in comments:
        reversed_comment.append(comment)
    reversed_comment.reverse()
    paginator = Paginator(reversed_comment,2)
    reversed_comment = paginator.get_page(page)
    hashtag = Hashtag.objects.filter(post_tag=post_id)
    A_M=ApplyMission.objects.filter(post=post_id)
    judge=False
    for a_m in A_M:
        if a_m.applier == request.user:
            judge=True
    
    scrap_users = post.user.all()
    total_scrap_user = scrap_users.count()

    return render(request, 'detail.html', {'post':post, 'comments': reversed_comment, 'hashtag':hashtag,'judge':judge, 'total_scrap_user':total_scrap_user})

def new(request):
    user = request.user
    hashtag = Hashtag.objects.all()
    return render(request, 'new.html', {'user':user, 'hashtag':hashtag})

def create(request):
    tmp=Profile.objects.get(profile_id=request.user.username)
    tmp1=request.POST['price']
    if tmp1 == '':
        tmp1=0
    tmp2=tmp.money
    tmp3=tmp2-int(tmp1)
    if tmp3 >= 0:
        tmp.money=tmp3
        tmp.save()
    else:
        error='금액이 부족합니다'
        return render(request,'new.html',{'error':error})
    new_post = Post()
    writer = request.user.username
    new_post.writer = writer
    new_post.title=request.POST['title']
    new_post.body=request.POST['body']
    new_post.pub_date = timezone.datetime.now()
    new_post.deposit=int(tmp1)
    
    if request.FILES.get('attached_img') is None:
        pass
    else:
        new_post.attached_img = request.FILES.get('attached_img')
    if request.FILES.get('attached_file') is None:
        pass
    else:
        new_post.attached_file = request.FILES.get('attached_file')

    new_post.save()
    
    applyMission = ApplyMission()
    applyMission.user=request.user
    applyMission.post = new_post
    applyMission.save()
    hash_list = request.POST['hashtag'].split('#')

    for index,hash in enumerate(hash_list):
        if index==0: #리스트의 첫번째값은 공백이므로 패스한다.
            pass
        else:
            if Hashtag.objects.filter(name=hash.upper()).exists():
                tag = Hashtag.objects.get(name=hash.upper())
                new_post.hashtag.add(tag)
            else:
                tag = Hashtag.objects.create(name=hash.upper())
                new_post.hashtag.add(tag)
    return redirect('request')

def edit(request, post_id):
    edit_post = Post.objects.get(id=post_id)
    post_tag = Hashtag.objects.filter(post_tag=post_id)
    all_tag = Hashtag.objects.all()

    checked_tag = []
    unchecked_tag = []
    for checked in post_tag:
        checked_tag.append(checked)
    for unchecked in all_tag:
        if unchecked in checked_tag:
            pass
        else:
            unchecked_tag.append(unchecked)

    return render(request, 'edit.html', {'post':edit_post, 'checked_tag':checked_tag, 'unchecked_tag':unchecked_tag})

def update(request, post_id):
    update_post = Post.objects.get(id=post_id)
    update_post.title = request.POST['title']
    update_post.body = request.POST['body']

    if request.FILES.get('attached_img') is None: #프로필 사진 form이 입력되지 않았을 시.
        pass
    else:
        update_post.attached_img = request.FILES.get('attached_img')

    if request.FILES.get('attached_file') is None:
        pass
    else:
        update_post.attached_file = request.FILES.get('attached_file')

    # Hashtag
    tag_list = request.POST.getlist('hashtag')
    add_hash_list = request.POST['add_hashtag'].split('#')
    update_post.hashtag.clear()
    
    for index,hsTag in enumerate(add_hash_list):
        if index==0: #리스트의 첫번째값은 공백이므로 패스한다.
            pass
        else:
            if hsTag.upper() in tag_list:
                pass
            else:
                tag_list.append(hsTag.upper())

    for tag in tag_list:
        if Hashtag.objects.filter(name=tag).exists():
            input_tag = Hashtag.objects.get(name=tag)
            update_post.hashtag.add(input_tag)
        else:
            input_tag = Hashtag.objects.create(name=tag)
            update_post.hashtag.add(input_tag)

    update_post.save()
    return redirect('request')

def delete(request, post_id):
    delete_post=Post.objects.get(id=post_id)
    delete_post.delete()
    return redirect('request')

def new_comment(request, post_id):
    comment = Comment()
    comment.writer = request.user.username
    comment.content = request.POST['content']
    comment.post = get_object_or_404(Post, pk=post_id)
    comment.save()
    
    post = Post.objects.get(pk=post_id)
    creator = request.user.profile
    to = Profile.objects.get(profile_id=post.writer)

    create_notification(creator, to, 'comment', comment.content, comment.post)

    return redirect('detail', post_id)

def comment_delete(request,comment_id):
    delete_comment=Comment.objects.get(id=comment_id)
    delete_comment.delete()
    return redirect('detail', delete_comment.post.pk)

def modify(request,comment_id):
    modify=Comment.objects.get(id=comment_id)
    modify.content=request.POST['modify_comment']

    modify.save()
    return redirect('detail', modify.post.pk)

def scrap(request,post_id):
    post=get_object_or_404(Post, pk = post_id)
    if post.user.filter(username=request.user.username).exists():
        post.user.remove(request.user)    
    else:
        post.user.add(request.user)
    post.save()
    return redirect('detail', post_id)

#수행자가 의뢰자의 미션 신청
def apply(request,post_id):
    post=Post.objects.get(id=post_id)
    applyMission = ApplyMission()
    applyMission.user=User.objects.get(username=post.writer)
    applyMission.post=Post.objects.get(id=post_id)
    applyMission.applier=request.user
    applyMission.save()

    creator = Profile.objects.get(profile_id=request.user.username)
    to = Profile.objects.get(profile_id=post.writer)
    create_notification(creator, to, 'mission_apply')

    return redirect('detail', post_id)

#의뢰자가 수행자의 미션신청을 승낙
def start(request,post_id,app_id):
    app=User.objects.get(username=app_id)
    mode=Post.objects.get(id=post_id)
    mode.status='running'
    mode.approved_id=app_id
    mode.save()
    tmp=ApplyMission.objects.filter(post=post_id,user=request.user.id)
    for n in tmp:
        if n.applier != app.id:
            n.applier= None

    creator = Profile.objects.get(profile_id=request.user.username) 
    to = Profile.objects.get(profile_id=app.username)
    create_notification(creator, to, 'mission_accept')

    return redirect('commissioned', profile_id=request.user.username)


#미션수행 완료
def end(request,post_id):
    mode=Post.objects.get(id=post_id)
    mode.status='completed'
    mode.save()
    tmp=Profile.objects.get(profile_id=mode.approved_id)
    tmp1=Profile.objects.get(profile_id=request.user.username)
    tmp.money+=tmp1.money
    tmp.save()
    profile=Profile.objects.get(profile_id=mode.approved_id)
    profile.mission_count+=1
    profile.save()

    review=Review()
    review.review_fk=tmp
    review.reviews=request.POST['review_content']
    try:
        review.ratings=int(request.POST['rating'])
    except MultiValueDictKeyError:
        review.ratings=0
    review.writer=request.user.username
    review.save()
    a_m=ApplyMission.objects.filter(post=post_id)

    creator = Profile.objects.get(profile_id=request.user.username) 
    to = Profile.objects.get(profile_id=mode.approved_id)
    create_notification(creator, to, 'mission_complete')

    for n in a_m:
        n.delete()
    return redirect('profile', tmp1.profile_id)

def tag_post(request, tag_id):
    tag_related_posts = Post.objects.filter(hashtag = tag_id)
    return render(request, 'tag_post.html', {'tag_posts':tag_related_posts})
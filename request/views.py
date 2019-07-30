from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment,ApplyMission
from hashtag.models import Hashtag
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from accounts.models import Profile
from mypage.models import MTM_chat,chatting,Review
from notification.views import create_notification
from django.core.exceptions import ObjectDoesNotExist



def like(request,post_id):
    post=get_object_or_404(B_Blog, pk = post_id)
    if post.user.filter(username=request.user.username).exists():
        post.user.remove(request.user)    
    else:
        post.user.add(request.user)
    post.save()
    return redirect('b_detail', post_id)

def apply(request,post_id):
    post=Post.objects.get(id=post_id)
    applyMission = ApplyMission()
    applyMission.user=User.objects.get(username=post.writer)
    applyMission.post=Post.objects.get(id=post_id)
    applyMission.applier=request.user
    applyMission.save()

    return redirect('detail', post_id)


def request_home(request):
    post_list=[]
    tmp= Post.objects.all()
    for n in tmp:
        if n.status != 'completed':
            post_list.append(n)
    
    if request.user.is_authenticated:
        my_scrap_post = Post.objects.filter(user = request.user)
        
        
    else:
        my_scrap_post = None
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    reversed_blogs= []
    for blog in blogs:
        reversed_blogs.append(blog)
    reversed_blogs.reverse()
    return render(request, 'request_home.html', {'blogs':blogs,'scrap_post':my_scrap_post,'reversed_blogs':reversed_blogs})
                                        

def detail(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments_list = Comment.objects.filter(post = post_id)
    paginator = Paginator(comments_list,10)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    reversed_comment=[]
    for comment in comments:
        reversed_comment.append(comment)
    reversed_comment.reverse()
    hashtag = Hashtag.objects.filter(post_tag=post_id)
    A_M=ApplyMission.objects.filter(post=post_id)
    judge=False
    for a_m in A_M:
        if a_m.applier == request.user:
            judge=True
    return render(request, 'detail.html', {'post':post, 'comments': reversed_comment, 'hashtag':hashtag,'judge':judge})

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
        return redirect('request')
    new_post = Post()
    writer = request.user.username
    new_post.writer = writer
    new_post.title=request.POST['title']
    new_post.body=request.POST['body']
    new_post.pub_date = timezone.datetime.now()

    new_post.attached_img = request.FILES.get('attached_img')
    new_post.deposit=int(tmp1)
    if request.FILES.get('attached_img') is None:
        new_post.attached_img = "https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwjauuWnxtXjAhXELqYKHf6tADQQjRx6BAgBEAU&url=http%3A%2F%2Fwww.sacscn.org.in%2FStaff.aspx&psig=AOvVaw1k5N6_SPjUTLxRWthDGbKQ&ust=1564332356410156"
    else:
        new_post.attached_img = request.FILES.get('attached_img')

    if request.FILES.get('attached_file') is None:
        new_post.attached_file = "https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwjauuWnxtXjAhXELqYKHf6tADQQjRx6BAgBEAU&url=http%3A%2F%2Fwww.sacscn.org.in%2FStaff.aspx&psig=AOvVaw1k5N6_SPjUTLxRWthDGbKQ&ust=1564332356410156"
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
    return render(request, 'edit.html', {'post':edit_post})

def update(request, post_id):
    update_post = Post.objects.get(id=post_id)
    update_post.title = request.POST['title']
    update_post.body = request.POST['body']
    if request.FILES.get('attached_img') is None: #프로필 사진 form이 입력되지 않았을 시.
        pass
    else:
        update_post.attached_img = request.FILES.get('attached_img')
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
    create_notification(creator, to, 'comment', comment.content)

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
    return redirect('commissioned', profile_id=request.user.username)



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
 
    review.ratings=int(request.POST['rating'])
    review.writer=request.user.username
    review.save()
    a_m=ApplyMission.objects.filter(post=post_id)
    for n in a_m:
        n.delete()
    try:
        chat=MTM_chat.objects.get(profile_fk=tmp.id,request_fk=tmp1.id)
        chat.delete()
        return redirect('profile', tmp1.profile_id)

    except ObjectDoesNotExist:

        return redirect('profile', tmp1.profile_id)

def tag_post(request, tag_id):
    tag_related_posts = Post.objects.filter(hashtag = tag_id)
    return render(request, 'tag_post.html', {'tag_posts':tag_related_posts})
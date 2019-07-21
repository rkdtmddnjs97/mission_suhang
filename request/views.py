from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Hashtag
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User


# Create your views here.

def request_home(request):
    post_list = Post.objects.all()
    if request.user.is_authenticated:
        my_scrap_post = Post.objects.filter(user = request.user)
    else:
        my_scrap_post = None
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    return render(request, 'request_home.html', {'blogs':blogs,'scrap_post':my_scrap_post})
                                        

def detail(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments_list = Comment.objects.filter(post = post_id)
    hashtag = Hashtag.objects.filter(tag=post_id)
    return render(request, 'detail.html', {'post':post, 'comments':comments_list, 'hashtag':hashtag})

def new(request):
    user = request.user
    hashtag = Hashtag.objects.all()
    return render(request, 'new.html', {'user':user, 'hashtag':hashtag})

def create(request):
    new_post = Post()
    writer = request.user.username
    new_post.writer = writer
    new_post.title=request.POST['title']
    new_post.body=request.POST['body']
    new_post.pub_date = timezone.datetime.now()
    new_post.save()

    #tag_temp=request.POST['hashtag'].upper()
    # print(type(tag_temp))
    # print(tag_temp)

    #list에 해시태그 분할저장
    hash_list = request.POST['hashtag'].split('#')

    for index,hash in enumerate(hash_list):
        if index==0: #리스트의 첫번째값은 공백이므로 패스한다.
            pass
        else:
            tag = Hashtag.objects.create(name=hash.upper())
            new_post.hashtag.add(tag)

    # tag = Hashtag.objects.create(name=request.POST['hashtag'].upper())
    # new_post.hashtag.add(tag)

    return redirect('request')

def edit(request, post_id):
    edit_post = Post.objects.get(id=post_id)
    return render(request, 'edit.html', {'post':edit_post})

def update(request, post_id):
    update_post = Post.objects.get(id=post_id)
    update_post.title = request.POST['title']
    update_post.body = request.POST['body']
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
    return redirect('detail', post_id)

def comment_delete(request,comment_id):
    delete_comment=Comment.objects.get(id=comment_id)
    delete_comment.delete()
    return redirect('detail', delete_comment.post.pk)
    #return redirect('detail', edit_comment.post.pk)

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

def start(request,post_id):
    mode=Post.objects.get(id=post_id)
    mode.status='running'
    mode.save()
    return redirect('detail', post_id)

def end(request,post_id):
    mode=Post.objects.get(id=post_id)
    mode.status='blocked'
    mode.save()
    return redirect('detail', post_id)

def tag_post(request, tag_id):
    tag_related_posts = Post.objects.filter(hashtag = tag_id)
    return render(request, 'tag_post.html', {'tag_posts':tag_related_posts})
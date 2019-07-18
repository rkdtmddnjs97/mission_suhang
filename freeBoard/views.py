from django.shortcuts import render, get_object_or_404, redirect
from .models import B_Blog,B_Comment
from django.utils import timezone
from django.contrib.auth.models import User

# Create your views here.
def board(request):
    Blogs = B_Blog.objects.all()
    return render(request, 'board.html', {'Blogs':Blogs})

def detail(request,post_id):
    blog = get_object_or_404(B_Blog, pk=post_id)
    comments_list = B_Comment.objects.filter(post = post_id)
    return render(request, 'b_detail.html', {'blog':blog,'comments':comments_list,'like_count':blog.total_likes})

def new(request):
    user = request.user
    return render(request, 'b_new.html', {'user':user})

def create(request):
    new_post = B_Blog()
    new_post.title=request.POST['title']
    writer = request.user.username
    new_post.writer = writer
    new_post.body=request.POST['body']
    new_post.pub_date = timezone.datetime.now()
    new_post.save()
    return redirect('board')

def edit(request, post_id):
    edit_post = B_Blog.objects.get(id=post_id)
    return render(request, 'b_edit.html', {'blog':edit_post})

def update(request, post_id):
    update_post = B_Blog.objects.get(id=post_id)
    update_post.title = request.POST['title']
    update_post.body = request.POST['body']
    update_post.save()
    return redirect('board')

def delete(request, post_id):
    delete_post=B_Blog.objects.get(id=post_id)
    delete_post.delete()
    return redirect('board')

def new_comment(request, post_id):
    comment = B_Comment()
    comment.writer = request.POST['writer']
    comment.content = request.POST['content']
    comment.post = get_object_or_404( B_Blog, pk=post_id)
    comment.save()
    return redirect('b_detail', post_id)

def like(request,post_id):
    post=get_object_or_404(B_Blog, pk = post_id)
    if post.user.filter(username=request.user.username).exists():
        post.user.remove(request.user)    
    else:
        post.user.add(request.user)
       
    post.save()
    return redirect('b_detail', post_id)

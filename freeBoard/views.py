from django.shortcuts import render, get_object_or_404, redirect
from .models import B_Blog,B_Comment
from django.utils import timezone
from hashtag.models import Hashtag
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# Create your views here.
def board(request):
    Blogs = B_Blog.objects.all()
    page = request.GET.get('page')
    reverse_blog = []
    for blog in Blogs:
        reverse_blog.append(blog)
    reverse_blog.reverse() 
    paginator = Paginator(reverse_blog,3)
    reverse_blog = paginator.get_page(page)  
    return render(request, 'board.html', { 'blogs':reverse_blog })

def detail(request,post_id):
    blog = get_object_or_404(B_Blog, pk=post_id)
    blog_like=[]
    for index,i in enumerate(blog.user.all()):
        if index != 5:
            blog_like.append(i)
    comments = B_Comment.objects.filter(post = post_id)
    page = request.GET.get('page')
    reversed_comments = []
    for comment in comments:
        reversed_comments.append(comment)
    reversed_comments.reverse()
    paginator = Paginator(reversed_comments,2)
    reversed_comments = paginator.get_page(page)
    hashtag = Hashtag.objects.filter(freeboard_tag=post_id)
    return render(request, 'b_detail.html', {'blog':blog,'comments':reversed_comments,'hashtag':hashtag,'like_count':blog.total_likes,'dislike_count':blog.total_dislikes,'blog_like':blog_like})

def new(request):
    user = request.user
    hashtag = Hashtag.objects.all()
    return render(request, 'b_new.html', {'user':user,'hashtag':hashtag})

def create(request):
    new_post = B_Blog()
    new_post.title=request.POST['title']
    writer = request.user.username
    new_post.writer = writer
    new_post.body=request.POST['body']
    new_post.pub_date = timezone.datetime.now()
    new_post.save()
    #list에 해시태그 분할저장
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

            # tag = Hashtag.objects.create(name=hash.upper())
            # new_post.hashtag.add(tag)
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
    comment.writer = request.user.username
    comment.content = request.POST['content']
    comment.post = get_object_or_404( B_Blog, pk=post_id)
    comment.save()
    return redirect('b_detail', post_id)

def comment_delete(request,comment_id):
    delete_comment=B_Comment.objects.get(id=comment_id)
    delete_comment.delete()
    return redirect('b_detail', delete_comment.post.pk)
    #return redirect('detail', edit_comment.post.pk)

def modify(request,comment_id):
    modify=B_Comment.objects.get(id=comment_id)
    modify.content=request.POST['modify_comment']
    modify.save()
    return redirect('b_detail', modify.post.pk)

def like(request,post_id):
    post=get_object_or_404(B_Blog, pk = post_id)
    if post.user.filter(username=request.user.username).exists():
        post.user.remove(request.user)    
    else:
        post.user.add(request.user)
       
    post.save()
    return redirect('b_detail', post_id)

def dislike(request,post_id):
    post=get_object_or_404(B_Blog, pk = post_id)
    if post.dislike.filter(username=request.user.username).exists():
        post.dislike.remove(request.user)    
    else:
        post.dislike.add(request.user)
       
    post.save()
    return redirect('b_detail', post_id)

def tag_post(request, tag_id):
    tag_related_posts = B_Blog.objects.filter(hashtag = tag_id)
    return render(request, 'b_tag_post.html', {'b_tag_posts':tag_related_posts})
def like_more(request,post_id):
    blog = get_object_or_404(B_Blog, pk=post_id)
    return render(request,'like_more.html',{'blog':blog})
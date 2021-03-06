from django.shortcuts import render, get_object_or_404, redirect
from .models import B_Blog,B_Comment
from django.utils import timezone
from hashtag.models import Hashtag
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Profile
# Create your views here.
def board(request):
    try:
        my_profile = Profile.objects.get(profile_id=request.user.username)
    except ObjectDoesNotExist:
        my_profile=None
    Blogs = B_Blog.objects.all()
    page = request.GET.get('page')
    reverse_blog = []
    for blog in Blogs:
        reverse_blog.append(blog)
    reverse_blog.reverse() 
    paginator = Paginator(reverse_blog, 9)
    total_len = len(reverse_blog)
    try:
       reverse_blog = paginator.get_page(page)
    except PageNotAnInterger:
       reverse_blog = paginator.page(1)
    except EmptyPage:
        reverse_blog = paginator.page(paginator.num_pages) 
    index = reverse_blog.number -1
    max_index = len(paginator.page_range)
    start_index = index -2 if index >= 2 else 0
    if index <2:
        end_index = 5 - start_index
    else:
        end_index = index+3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])

    return render(request, 'board.html', { 'blogs':reverse_blog, 'page_range':page_range, 'total_len':total_len,'max_index':max_index-2, 'my_profile':my_profile})

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
    if request.FILES.get('attached_img') is None:
        pass
    else:
        new_post.attached_img = request.FILES.get('attached_img')
    if request.FILES.get('attached_file') is None:
        pass
    else:
        new_post.attached_file = request.FILES.get('attached_file')
    new_post.save()

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
    return redirect('board')

def edit(request, post_id):
    edit_post = B_Blog.objects.get(id=post_id)
    post_tag = Hashtag.objects.filter(freeboard_tag=post_id)
    all_tag = Hashtag.objects.all()

    checked_tag = []
    for checked in post_tag:
        checked_tag.append(checked)

    return render(request, 'b_edit.html', {'edit_post':edit_post, 'checked_tag':checked_tag, 'all_tag':all_tag })

def update(request, post_id):
    update_post = B_Blog.objects.get(id=post_id)
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
    return redirect('b_detail', post_id)

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
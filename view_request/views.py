from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .forms import NewBlog


def welcome(request):
    return render(request, 'viewcrud/index.html')

def read(request):
    #페이지네이터기능
    #blogs=Blog.objects.all()
    blogs = Blog.objects
    blog_list = Blog.objects.all()
    #페이지 자르기
    paginator = Paginator(blog_list,5)
    page=request.GET.get('page')
    posts=paginator.get_page(page)
    return render(request, 'viewcrud/funccrud.html',{'blogs':blogs, 'posts':posts})

def create(request):
    #새로운 글쓰기 == POST
    if request.method =='POST':
       form=NewBlog(request.POST)
       if form.is_valid:
           post=form.save(commit=False)
           post.pub_date=timezone.now()
           post.save()
           return redirect('home1')

    #입력된 글 저장하기


    #글쓰기 페이지를 띄워주는 역할 ==GET(!==POST)
    else:
      #단순히 입력 받을 수 있는 form을 띄워라 
      form = NewBlog()
      return render(request,'viewcrud/new.html',{'form':form}) 


    return

def update(request,pk):

    blog = get_object_or_404(Blog,pk=pk)

    form = NewBlog(request.POST, instance=blog)

    if form.is_valid():
        form.save()
        return redirect('home1')

    return render(request,'viewcrud/new.html',{'form':form})

def delete(request,pk):
    blog=get_object_or_404(Blog,pk=pk)
    blog.delete()
    return redirect('home1')

def detail(request,pk):
    blog_detail= get_object_or_404(Blog,pk=pk)
    return render(request,'viewcrud/detail.html',{'blog':blog_detail})
# Create your views here.

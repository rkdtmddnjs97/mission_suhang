from django.shortcuts import render, get_object_or_404, redirect
from request.models import Post,ApplyMission,submit_form
from accounts.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User

# Create your views here.


def personal(request):
    # my_profile = Profile.objects.all()
    my_profile = request.user.profile
    user = request.user

    return render(request, 'profile.html', {'my_profile':my_profile, 'user':user})
    # return render(request, 'profile.html')

def commissioned(request):
    commissioned_post=ApplyMission.objects.filter( user=request.user)
    
    applications=[]
    notNone=[]
    for application in commissioned_post:
        if application.applier is None :

            applications.append(Post.objects.get(id=application.post.id))
        else:
            notNone.append(application)
    appliers=[]

    applicants=[]
    for applie in notNone:
        pro=Profile.objects.get(user=applie.applier)
        pro.connector=applie.post.id
        appliers.append(pro)
    
    return render(request, 'commissioned.html',{'applications':applications,'appliers':appliers})

def performing(request):
    performing_post= Post.objects.filter(approved_id=request.user.username)
   

    
    return render(request, 'performing.html',{'performing_post':performing_post})

def scrap(request):
    #request앱 Post모델객체 사용
    my_scraped_post = Post.objects.filter(user = request.user)

    return render(request, 'scrap.html', {'scraped_post':my_scraped_post})


def editProfile(request):
    userProfile = request.user.profile
    return render(request, 'editProfile.html', {'userProfile': userProfile})

def updateProfile(request):
    #user = User.objects.get(pk=user_id)
    user = request.user
    
    user.profile.university=request.POST['university']
    user.profile.department=request.POST['department']
    user.profile.name=request.POST['name']
    user.profile.nickname=request.POST['nickname']
    user.profile.introduction=request.POST['introduction']
    user.save()
    return redirect('profile')
def submit_page(request,post_id):
     post=Post.objects.get(id=post_id)
     return render(request, 'submit.html',{'post':post})
def submit_send(request,post_id):
    form=submit_form()
    form.pub_date=timezone.datetime.now()
    form.writer=request.POST['writer']
    form.title=request.POST['title']
    form.body=request.POST['body']
    form.submit=Post.objects.get(id=post_id)
    form.save()
    post=Post.objects.get(id=post_id)
    post.s_flag=True
    post.save()
    return redirect('performing')

def submission(request,post_id):
    submission_result=submit_form.objects.get(submit=post_id)
    return render(request,'submission.html',{'submission_result':submission_result})
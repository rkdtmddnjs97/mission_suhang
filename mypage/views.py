from django.shortcuts import render, get_object_or_404, redirect
from request.models import Post,ApplyMission
from accounts.models import Profile
from django.contrib.auth.models import User
from hashtag.models import Hashtag

# Create your views here.


def personal(request):
    my_profile = request.user.profile
    user = request.user
    tag_list = my_profile.hashtag.all()

    return render(request, 'profile.html', {'my_profile':my_profile, 'user':user, 'tag_list':tag_list })

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
    return render(request, 'performing.html')

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
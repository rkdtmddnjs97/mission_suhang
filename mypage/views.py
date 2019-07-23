from django.shortcuts import render, get_object_or_404, redirect
from request.models import Post,ApplyMission
from accounts.models import Profile
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
    connector=[]
    for applie in notNone:
        appliers.append(Profile.objects.filter(user=applie.applier))
        connector.append(applie.post.id)
    
   
    print(connector)
    print(appliers)
    return render(request, 'commissioned.html',{'applications':applications,'appliers':appliers,'connector':connector})

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
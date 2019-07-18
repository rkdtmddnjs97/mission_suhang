from django.shortcuts import render, get_object_or_404, redirect
from view_request.models import Blog
from accounts.models import Profile
#from .models import Blog
# Create your views here.


#import 가 답이 안나와서..

def profile(request):
    # my_profile = Profile.objects.all()
    my_profile = request.user.profile

    return render(request, 'profile.html', {'my_profile':my_profile})
    # return render(request, 'profile.html')

def commissioned(request):
    return render(request, 'commissioned.html')

def performing(request):
    return render(request, 'performing.html')

def scrap(request):
    #view_request앱 Blog모델객체 사용
    my_scraped_post = Blog.objects.filter(user = request.user)

    return render(request, 'scrap.html', {'scraped_post':my_scraped_post})


def editProfile(request):
    return render(request, 'editProfile.html')
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
# from view_request.models import Blog

#import 가 답이 안나와서..

def profile(request):

    return render(request, 'profile.html')

def commissioned(request):
    return render(request, 'commissioned.html')

def performing(request):
    return render(request, 'performing.html')

def scrap(request):
    #여기에서 view_request앱 모델의 Blog 객체를 쓰려고하는데...
    #my_scraped_post = Blog.objects.filter(user = request.user)

    return render(request, 'scrap.html')
    #return render(request, 'scrap.html', {'scraped_post':my_scraped_post})

def editProfile(request):
    return render(request, 'editProfile.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile
from hashtag.models import Hashtag
import string
import random

def signup(request):
    all_hashtag = Hashtag.objects.all()
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            _LENGTH = 8 # 20자리
 
            # 숫자 + 대소문자 + 특수문자
            string_pool = string.ascii_letters + string.digits + string.punctuation
 
            # 랜덤한 문자열 생성
            result = "인증번호:" 
            for i in range(_LENGTH) :
                result += random.choice(string_pool) # 랜덤한 문자열 하나 선택


            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            
            user.profile.university=request.POST['university']
            user.profile.department=request.POST['department']
            user.profile.name=request.POST['name']
            user.profile.introduction=request.POST['introduction']
            user.profile.email=request.POST['email']
            user.profile.profile_id=request.POST['username']
            user.profile.ssn=result.split(':')[1]
            
            tag_list = request.POST.getlist('hashtag')
            for tag in tag_list:
                input_tag = Hashtag.objects.get(name=tag.upper())
                user.profile.hashtag.add(input_tag)
            
            user.save()
            
            email = EmailMessage('인증 메일', result , to=[request.POST['email']])
            email.send()
            return render(request,'approval.html')
    return render(request, 'signup.html', {'hashtag':all_hashtag})

def approve(request):
    if request.user.profile.ssn == request.POST['ssn']:

    
        if request.user.profile.approval == False:
            request.user.profile.approval=True
            
    else:
        request.user.delete()
        

    return redirect('home')  

    

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return render(request, 'signup.html')




  
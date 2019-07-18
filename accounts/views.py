from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile
import string
import random

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            _LENGTH = 8 # 20자리
 
# 숫자 + 대소문자 + 특수문자
            string_pool = string.ascii_letters + string.digits + string.punctuation
 
# 랜덤한 문자열 생성
            result = "" 
            for i in range(_LENGTH) :
                result += random.choice(string_pool) # 랜덤한 문자열 하나 선택


            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            
            user.profile.university=request.POST['university']
            user.profile.department=request.POST['department']
            user.profile.name=request.POST['name']
            user.profile.nickname=request.POST['nickname']
            user.profile.introduction=request.POST['introduction']
            user.profile.email=request.POST['email']
            user.profile.ssn=result

            user.save()
            
            email = EmailMessage('subject text', result , to=[request.POST['email']])
            email.send()
            return render(request,'approval.html')
    return render(request, 'signup.html')

def approve(request):

    if request.user.profile.approval == False:
         if request.user.profile.ssn == request.POST['ssn']:
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




  
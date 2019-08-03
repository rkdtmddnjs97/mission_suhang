from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile
from hashtag.models import Hashtag
import string
import random
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.exceptions import ObjectDoesNotExist


def signup(request):
    all_hashtag = Hashtag.objects.all()
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:

            _LENGTH = 8  # 20자리
            string_pool = string.ascii_letters + string.digits 
                # 숫자 + 대소문자 + 특수문자
            result =''
            for i in range(_LENGTH):
                result+=random.choice(string_pool)
                 # 랜덤한 문자열 하나 선택
            try:
                 user = User.objects.create_user(
                 username=request.POST['username'], password=request.POST['password1'])
                 auth.login(request, user)
            except IntegrityError:
                error1='아이디가 이미 존재합니다.'
                return render(request, 'signup.html', {'hashtag': all_hashtag,'error1':error1})
            school={'국민대학교': 'kookmin.ac.kr'}
            tmp=request.POST['email'].split('@')[1]
            tmp1=school[request.POST['university']] 
            print(tmp1)
            print(tmp)
            if tmp == tmp1:

                pass
            else:
                error2='학교가 안맞습니다.'
                return render(request,'signup.html', {'hashtag': all_hashtag,'error2':error2})

            user.profile.university = request.POST['university']
            user.profile.department = request.POST['department']
            user.profile.name = request.POST['name']
            user.profile.introduction = request.POST['introduction']
            user.profile.email = request.POST['email']
            user.profile.profile_id = request.POST['username']
            user.profile.ssn = result
            user.profile.profile_img = request.FILES.get('pofile_img')

            # 프로필 사진 form이 입력되지 않았을 시 마이페이지 에러를 방지하기 위해 더미이미지를 넣도록 함.
            if request.FILES.get('profile_img') is None:
                user.profile.profile_img = "https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwjauuWnxtXjAhXELqYKHf6tADQQjRx6BAgBEAU&url=http%3A%2F%2Fwww.sacscn.org.in%2FStaff.aspx&psig=AOvVaw1k5N6_SPjUTLxRWthDGbKQ&ust=1564332356410156"
            else:
                user.profile.profile_img = request.FILES.get('pofile_img')
                
            tag_list = request.POST.getlist('hashtag')
            for tag in tag_list:
                input_tag = Hashtag.objects.get(name=tag.upper())
                user.profile.hashtag.add(input_tag)

            user.save()
            html_content=render_to_string('email_approval.html',{'result':result})
            message = strip_tags(html_content)
            email = EmailMultiAlternatives('인증 메일', message, to=[request.POST['email']])
            email.attach_alternative(html_content, "text/html")
            email.send()
            return render(request, 'approval.html')
        else:
              error='비밀번호가 일치하지 않습니다.'
              return render(request, 'signup.html', {'hashtag': all_hashtag,'error':error})
    return render(request, 'signup.html', {'hashtag': all_hashtag})


def approve(request):
    if request.user.profile.ssn == request.POST['ssn']:
        if request.user.profile.approval == False:
            request.user.profile.approval = True
            request.user.profile.save()
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
    
            if request.user.profile.approval == True or request.user.is_superuser ==True:
                    return redirect('home')
            else:
                    request.user.delete()
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

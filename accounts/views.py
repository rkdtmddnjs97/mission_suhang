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
            school={'국민대학교': 'kookmin.ac.kr','가천대학교':'gachon.ac.kr','경남대학교':'kangnam.ac.kr',
            '강원대학교':'kangwon.ac.kr','건국대학교':'konkuk.ac.kr','건양대학교':'konyang.ac.kr','경기대학교':'kyonggi.ac.kr',
            '경북대학교':'knu.ac.kr','경상대학교':'gnu.ac.kr','경성대학교':'ks.ac.kr','경희대학교':'khu.ac.kr',
            '고려대학교':'korea.ac.kr','광운대학교':'kw.ac.kr','남서울대학교':'nsu.ac.kr','단국대학교':'dankook.ac.kr',
            '덕성여자대학교':'duksung.ac.kr','동국대학교':'dongguk.edu','동덕여자대학교':'dongduk.ac.kr','명지대학교':'mju.ac.kr',
            '목포대학교':'mokpo.ac.kr','부산대학교':'pusan.ac.kr','삼육대학교':'syu.ac.kr','상명대학교':'smu.ac.kr','서강대학교':'sogang.ac.kr',
            '서울대학교':'snu.ac.kr','서울시립대학교':'uos.ac.kr','서울여자대학교':'swu.ac.kr','선문대학교':'sunmoon.ac.kr',
            '성공회대학교':'skhu.ac.kr','성균관대학교':'skku.edu','성신여자대학교':'sungshin.ac.kr','세종대학교':'sejong.ac.kr',
            '숙명여자대학교':'sookmyung.ac.kr','아주대학교':'ajou.ac.kr','연세대학교':'yonsei.ac.kr','영남대학교':'yu.ac.kr',
            '원광대학교':'wku.ac.kr','이화여자대학교':'ewha.ac.kr','인천대학교':'inu.ac.kr','인하대학교':'inha.ac.kr',
            '전북대학교':'chonbuk.ac.kr','조선대학교':'chosun.kr','중앙대학교':'cau.ac.kr','충남대학교':'cnu.ac.kr',
            '충북대학교':'cbnu.ac.kr','평택대학교':'ptu.ac.kr','한국산업기술대학교':'kpu.ac.kr','한국외국어대학교':'hufs.ac.kr',
            '한국항공대학교':'kau.ac.kr','한밭대학교':'hanbat.ac.kr','한양대학교':'hanyang.ac.kr','홍익대학교':'hongik.ac.kr',
            '대구경북과학기술원':'dgist.ac.kr','울산과학기술원':'unist.ac.kr','계명대학교':'kmu.ac.kr','동신대학교':'dsu.ac.kr',
            '명지대학교':'mju.ac.kr','순천향대학교':'sch.ac.kr','한국교원대학교':'knue.ac.kr','한국교통대학교':'ut.ac.kr',
            '멋쟁이사자처럼':'likelion.org'}
            try:
                Profile.objects.get(email=request.POST['email'])
                error4='이메일이 이미 존재합니다' 
                return render(request,'signup.html', {'hashtag': all_hashtag,'error4':error4})
            except ObjectDoesNotExist:
                pass
            tmp=request.POST['email'].split('@')[1]
            try:
                tmp1=school[request.POST['university']] #해당 대학교가 없습니다
            except KeyError:
                error3='해당 대학교가 없습니다'
                return render(request,'signup.html', {'hashtag': all_hashtag,'error3':error3})
            
            if tmp == tmp1:

                pass
            else:
                error2='학교가 안맞습니다.'
                return render(request,'signup.html', {'hashtag': all_hashtag,'error2':error2})
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
            

            user.profile.university = request.POST['university']
            user.profile.department = request.POST['department']
            user.profile.name = request.POST['name']
            user.profile.introduction = request.POST['introduction']
            user.profile.email = request.POST['email']
            user.profile.profile_id = request.POST['username']
            user.profile.ssn = result
            user.profile.profile_img = request.FILES.get('pofile_img')
                
            tag_list = request.POST.getlist('hashtag')
            for tag in tag_list:
                input_tag = Hashtag.objects.get(name=tag.upper())
                user.profile.hashtag.add(input_tag)

            user.profile.save()
        
            html_content=render_to_string('email_approval.html',{'result':result})
            message = strip_tags(html_content)
            email = EmailMultiAlternatives('인증 메일', message, to=[request.POST['email']])
            email.attach_alternative(html_content, "text/html")
            email.send()
            judge='False'
            left_time=180
            return render(request, 'approval.html',{'judge':judge,'left_time':left_time})
        else:
              error='비밀번호가 일치하지 않습니다.'
              return render(request, 'signup.html', {'hashtag': all_hashtag,'error':error})
    return render(request, 'signup.html', {'hashtag': all_hashtag})


def approve(request):
    if request.POST['flag']=='True':       
        if request.user.profile.ssn == request.POST['ssn']:
            if request.user.profile.approval == False:
                request.user.profile.approval = True
                if request.user.profile.email.split('@')[1]=='likelion.org':
                    request.user.profile.money=4000
                request.user.profile.save()
        else:
            request.user.delete()
        return redirect('home')
    elif request.POST['flag']=='False':
         if request.user.profile.ssn == request.POST['ssn']:
            if request.user.profile.approval == False:
                request.user.profile.approval = True
                if request.user.profile.email.split('@')[1]=='likelion.org':
                    request.user.profile.money=4000
                request.user.profile.save()
                return redirect('home')
         else:
            error='인증번호가 틀립니다.'
            left_time=request.POST['time']
            judge='False'            
            return render(request,'approval.html',{'error':error,'left_time':left_time,'judge':judge})


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

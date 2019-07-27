from django.shortcuts import render, get_object_or_404, redirect
from request.models import Post,ApplyMission,submit_form
from accounts.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User
from hashtag.models import Hashtag
from .models import MTM_chat,chatting
from django.core.exceptions import ObjectDoesNotExist


# def search(request):
#     input_data = request.GET['input_data'].upper()
#     try:
#         tag = Hashtag.objects.get(name=input_data)
#         results = Post.objects.filter(hashtag=tag)
#         result_flag = True
#         return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag})

#     except ObjectDoesNotExist:
#         results = '검색 결과가 없습니다^^'
#         result_flag = False
#         return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag})

def chat(request,app_id,request_id):
  
    #room=MTM_chat.objects.filter()
    try:
        

        chat_room=MTM_chat.objects.get(profile_fk=app_id,request_fk=request_id)
        chat_objects=chatting.objects.filter(chatting_fk=chat_room.id)
    
    except ObjectDoesNotExist:

      
      
        chat_room=MTM_chat()
        chat_room.profile_fk=Profile.objects.get(id=app_id)
        chat_room.request_fk=Profile.objects.get(id=request_id)
        chat_room.save()

        chat_objects=chatting.objects.filter(chatting_fk=chat_room.id)
    
    return render(request,'chatting.html',{'chat_objects':chat_objects,'chat_id':chat_room.id,'app_id':app_id,'request_id':request_id})

def new_chat(request,chat_id):
    tmp=chatting()
    tmp.chatting_fk=MTM_chat.objects.get(id=chat_id)
    tmp.writer=request.POST['writer']
    tmp.content=request.POST['content']
    tmp.save()
    app_id=request.POST['app_id']
    request_id=request.POST['request_id']
    return redirect('chat',app_id,request_id)

def chat_delete(request,chat_id,appId,requestId):
    tmp=chatting.objects.get(id=chat_id)
    tmp.delete()
    return redirect('chat',appId,requestId)
def chat_edit(request,chat_id,appId,requestId):
    tmp=chatting.objects.get(id=chat_id)
    tmp.content=request.POST['modify_chat']
    tmp.save()
    return redirect('chat',appId,requestId)
    
def personal(request):
    my_profile = request.user.profile
    tag_list = my_profile.hashtag.all()

    return render(request, 'profile.html', {'my_profile':my_profile, 'tag_list':tag_list})
def disagree(request,post_id,app_id):
    tmp=User.objects.get(username=app_id)
    eleminate=ApplyMission.objects.get( user=request.user,post=post_id,applier=tmp.id)
    eleminate.delete()
    return redirect('commissioned')
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
    connectors=[]
    for applie in notNone:
        pro=Profile.objects.get(user=applie.applier)
        connectors.append(applie.post.id)
        appliers.append(pro)
        
    commission_user=Profile.objects.get(profile_id=request.user.username)

    return render(request, 'commissioned.html',{'applications':applications,'appliers':appliers,'commission_user':commission_user,'connectors':connectors})

def performing(request):
    performing_post= Post.objects.filter(approved_id=request.user.username)
    perform_profiles=[]
    for perform in performing_post:
        perform_profiles.append(Profile.objects.get(profile_id=perform.writer))
    perform_user=Profile.objects.get(profile_id=request.user.username)
    
    return render(request, 'performing.html',{'performing_post':performing_post,'perform_profiles':perform_profiles,'perform_user':perform_user})

def scrap(request):
    #request앱 Post모델객체 사용
    my_scraped_post = Post.objects.filter(user = request.user)

    return render(request, 'scrap.html', {'scraped_post':my_scraped_post})


def editProfile(request):
    userProfile = request.user.profile
    my_tag = userProfile.hashtag.all()
    all_tag = Hashtag.objects.all()
    checked_tag = []
    uncheked_tag = []
    for checked in my_tag:
        checked_tag.append(checked)
    for unchecked in all_tag:
        if unchecked in checked_tag:
            pass
        else:
            uncheked_tag.append(unchecked)
    
    return render(request, 'editProfile.html', {'userProfile': userProfile, 'checked_tag':checked_tag, 'unchecked_tag':uncheked_tag})

def updateProfile(request):
    #user = User.objects.get(pk=user_id)
    user = request.user
    
    user.profile.university=request.POST['university']
    user.profile.department=request.POST['department']
    user.profile.name=request.POST['name']
    user.profile.introduction=request.POST['introduction']
    
    if request.FILES.get('pofile_img') is None: #프로필 사진 form이 입력되지 않았을 시.
        pass
    else:
        user.profile.profile_img = request.FILES.get('pofile_img')

    tag_list = request.POST.getlist('hashtag')
    for tag in tag_list:
        input_tag = Hashtag.objects.get(name=tag.upper())
        user.profile.hashtag.add(input_tag)

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

def recharge(request,profile_id):
    money=request.POST['charge_money']
    profile=profile_id
    return render(request,'charge.html',{'money':money,'profile':profile})

def calculate(request,profile_id,cash):
    tmp=Profile.objects.get(id=profile_id)
    tmp1=int(cash)
    tmp2=tmp.money
    tmp.money=tmp1+tmp2
    tmp.save()
    return redirect('profile')
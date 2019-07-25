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
        

        tmp1=MTM_chat.objects.get(profile_fk=app_id,request_fk=request_id)
        chat_objects=chatting.objects.filter(chatting_fk=tmp1.id)
    
    except ObjectDoesNotExist:

        tmp=chatting()
      
        chat_room=MTM_chat()
        chat_room.profile_fk=Profile.objects.get(id=app_id)
        chat_room.request_fk=Profile.objects.get(id=request_id)
        chat_room.save()
        tmp=chatting()
        tmp.chatting_fk=chat_room
        tmp.save()
        chat_objects=chatting.objects.filter(chatting_fk=chat_room.id)
    
    return render(request,'chatting.html',{'chat_objects':chat_objects})


    
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
    commission_user=Profile.objects.get(profile_id=request.user.username)

    return render(request, 'commissioned.html',{'applications':applications,'appliers':appliers,'commission_user':commission_user})

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


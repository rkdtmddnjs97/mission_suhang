from django.shortcuts import render, get_object_or_404, redirect
from request.models import Post,ApplyMission,submit_form
from accounts.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User
from hashtag.models import Hashtag
from .models import MTM_chat,chatting,Review,complaint
from django.core.exceptions import ObjectDoesNotExist
from notification.views import create_notification


def chat(request,app_id,request_id):
  
    #room=MTM_chat.objects.filter()
    try:
        chat_room=MTM_chat.objects.get(profile_fk=app_id,request_fk=request_id)
        chat_objects=chatting.objects.filter(chatting_fk=chat_room.id)
    
    except ObjectDoesNotExist:
        try:
             chat_room=MTM_chat.objects.get(profile_fk=request_id,request_fk=app_id)
        except ObjectDoesNotExist:
             chat_room=MTM_chat()
             chat_room.profile_fk=Profile.objects.get(id=request_id)
             chat_room.request_fk=Profile.objects.get(id=app_id)
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

    request_user = Profile.objects.get(id=request_id)
    app_user = Profile.objects.get(id=app_id)

    if tmp.writer == request_user.profile_id:
        creator = request_user
        to = app_user
        create_notification(creator, to, 'chat', tmp.content)
    else:
        creator = app_user
        to = request_user
        create_notification(creator, to, 'chat', tmp.content)

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

#의뢰자가 수행자의 미션신청을 거절
def disagree(request,post_id,app_id):
    apply=User.objects.get(username=app_id)
    eleminate=ApplyMission.objects.get(user=request.user, post=post_id, applier=apply.id)
    eleminate.delete()

    creator = Profile.objects.get(profile_id=request.user.username) 
    to = Profile.objects.get(profile_id=apply.username)
    create_notification(creator, to, 'mission_reject')

    return redirect('commissioned', profile_id=request.user.username)

def commissioned(request, profile_id):
    user = User.objects.get(username=profile_id)
    commissioned_post=ApplyMission.objects.filter(user=user)
    
    applications=[]
    notNone=[]
    for application in commissioned_post:
        
        if application.applier is None :
            tmp=Post.objects.get(id=application.post.id)
            if tmp.status != 'completed':
                applications.append(tmp)
        else:
            notNone.append(application)
    appliers=[]
    applicants=[]
   
    for applie in notNone:
        pro=Profile.objects.get(user=applie.applier)
        pro.connector=applie.post.id
        pro.save()
        appliers.append(pro)
        
    commission_user=Profile.objects.get(profile_id=profile_id)

    return render(request, 'commissioned.html',{'applications':applications,'appliers':appliers,'commission_user':commission_user})

def performing(request, profile_id):
    user=User.objects.get(username=profile_id)
    tmp=ApplyMission.objects.filter(applier=user.id)
    # Post.objects.filter(approved_id=request.user.username)
    performing_post=[]
    for n in tmp:
        tmp1=Post.objects.get(id=n.post.id)
        if tmp1.status != 'completed':
            performing_post.append(tmp1)
    perform_profiles=[]
    for perform in performing_post:
        perform_profiles.append(Profile.objects.get(profile_id=perform.writer))
    perform_user=Profile.objects.get(profile_id=user.username)
    
    return render(request, 'performing.html',{'performing_post':performing_post,'perform_profiles':perform_profiles,'perform_user':perform_user})

def scrap(request, profile_id):
    user = User.objects.get(username = profile_id)
    profile = profile_id
    my_scraped_post = Post.objects.filter(user = user)

    return render(request, 'scrap.html', {'scraped_post':my_scraped_post, 'profile':profile})

def myProfile(request, profile_id):
    user_profile=Profile.objects.get(profile_id=request.user.username)
    my_profile = Profile.objects.get(profile_id=profile_id)
    tag_list = my_profile.hashtag.all()
    review_objects=Review.objects.filter(review_fk=my_profile.id)
    
    number=review_objects.count()
   
    average_rate=0
    for rate in review_objects:
        average_rate+=rate.ratings
    try:
        average_rate/=number
    except ZeroDivisionError:
        average_rate=0
    return render(request, 'profile.html', {'my_profile':my_profile, 'tag_list':tag_list,'review_objects':review_objects,'average_rate':average_rate,'number':number,'user_profile':user_profile})


def editProfile(request, profile_id):
    if request.user.profile.profile_id==profile_id:
        userProfile = Profile.objects.get(profile_id=profile_id)
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
    else:
        print("본인 계정이 아니면 접근할 수 없습니다.") #나중에 html 경고창 띄우게 수정하면 참 좋을 듯ㅎㅎ
        return redirect('profile', profile_id=profile_id)

def updateProfile(request, profile_id):
    update_profile = Profile.objects.get(profile_id=profile_id)
    
    update_profile.university=request.POST['university']
    update_profile.department=request.POST['department']
    update_profile.name=request.POST['name']
    update_profile.introduction=request.POST['introduction']
    
    if request.FILES.get('pofile_img') is None: #프로필 사진 form이 입력되지 않았을 시.
        pass
    else:
        update_profile.profile_img = request.FILES.get('pofile_img')

    tag_list = request.POST.getlist('hashtag')
    update_profile.hashtag.clear()

    for tag in tag_list:
        input_tag = Hashtag.objects.get(name=tag.upper())
        update_profile.hashtag.add(input_tag)

    update_profile.save()

    return redirect('profile', profile_id=profile_id)

def submit_page(request,post_id):
     post=Post.objects.get(id=post_id)
     return render(request, 'submit.html',{'post':post})

def submit_send(request,post_id):
    form=submit_form()
    form.pub_date=timezone.datetime.now()
    form.writer=request.POST['writer']
    form.title=request.POST['title']
    form.body=request.POST['body']
    if request.FILES.get('attachment') is None:
        form.attachment = "https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwjauuWnxtXjAhXELqYKHf6tADQQjRx6BAgBEAU&url=http%3A%2F%2Fwww.sacscn.org.in%2FStaff.aspx&psig=AOvVaw1k5N6_SPjUTLxRWthDGbKQ&ust=1564332356410156"
    else:
        form.attachment = request.FILES.get('attachment')
        
    form.submit=Post.objects.get(id=post_id)
    form.save()
    post=Post.objects.get(id=post_id)
    post.s_flag=True
    post.save()

    creator = Profile.objects.get(profile_id=request.user.username) 
    to = Profile.objects.get(profile_id=post.writer)
    create_notification(creator, to, 'mission_submit')

    return redirect('performing', profile_id=request.user.username)

def submission(request,post_id):
    post=Post.objects.get(id=post_id)
    submission_result=submit_form.objects.get(submit=post_id)
    return render(request,'submission.html',{'submission_result':submission_result,'post':post})

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
    return redirect('profile', profile_id=profile_id)

def mission_quit(request,post_id):
    mode=Post.objects.get(id=post_id)
    mode.status='ready'
    mode.approved_id=None
    mode.save()
    tmp=User.objects.get(username=mode.writer)
    tmp1=ApplyMission.objects.get(user=tmp.id,post=mode.id,applier=request.user.id)
    tmp1.delete()
    return redirect('performing', profile_id=request.user.username)

def submission_edit(request,submission_id,postId):
    tmp=submit_form.objects.get(id=submission_id)
    tmp.body=request.POST['content']
    tmp.save()
    return redirect('submission', postId)
    # def submission(request,post_id):
    # submission_result=submit_form.objects.get(submit=post_id)
    # return render(request,'submission.html',{'submission_result':submission_result})

def commission_quit(request,post_id):
    tmp=Post.objects.get(id=post_id)
    tmp.delete()
    return redirect('commissioned', profile_id=request.user.username)

def performing_end(request,profile_id):
    tmp=Post.objects.filter(approved_id=profile_id)
    blocked_posts=[]
    for n in tmp:
        if n.status == 'completed':
            blocked_posts.append(n)


    return render(request,'perform_end.html',{'blocked_posts':blocked_posts,'profile_id':profile_id})
def commission_end(request,profile_id):
    tmp=Post.objects.filter(writer=request.user.username)
    blocked_posts=[]
    for n in tmp:
        if n.status == 'completed':
            blocked_posts.append(n)
    return render(request,'perform_end.html',{'blocked_posts':blocked_posts,'profile_id':profile_id})
def submit_result(request,post_id):
    form_result=submit_form.objects.get(submit=post_id)
    return render(request,'submit_result.html',{'form_result':form_result})
def delete_final(request, post_id,app_id):
    delete_post=Post.objects.get(id=post_id)
    delete_post.delete()
    return redirect('performing_end',app_id)
def complain(request,profile_id):
    prey_profile=Profile.objects.get(id=profile_id)
    complainer_profile=Profile.objects.get(profile_id=request.user.username)
    complaints=complaint()
    complaints.complainer=complainer_profile
    complaints.prey=prey_profile
    complaints.casuse=request.POST['complain_content']
    complaints.save()
    return redirect('profile',prey_profile.profile_id)


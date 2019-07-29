from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<str:profile_id>/', views.myProfile, name="profile"),
    path('commissioned/<str:profile_id>', views.commissioned, name="commissioned"),
    path('performing/<str:profile_id>', views.performing, name="performing"),
    path('scrap/<str:profile_id>', views.scrap, name="scrap"),
    path('editProfile/<str:profile_id>', views.editProfile, name="editProfile"),
    path('updateProfile/<str:profile_id>', views.updateProfile, name="updateProfile"),
    path('submit_page/<int:post_id>', views.submit_page, name="submit_page"),
    path('submit_send/<int:post_id>', views.submit_send, name="submit_send"),
    path('submission/<int:post_id>', views.submission, name="submission"),
    path('chat/<app_id> <request_id>', views.chat, name="chat"),
    path('disagree/<post_id> <app_id>', views.disagree, name="disagree"),
    path('new_chat/<int:chat_id>', views.new_chat, name="new_chat"),
    path('chat_delete/<chat_id> <appId> <requestId>', views.chat_delete, name="chat_delete"),
    path('chat_edit/<chat_id> <appId> <requestId>', views.chat_edit, name="chat_edit"),
    path('recharge/<int:profile_id>', views.recharge, name="recharge"),
    path('calculate/<profile_id> <cash>', views.calculate, name="calculate"),
    path('mission_quit/<int:post_id>', views.mission_quit, name="mission_quit"),
    path('submission_edit/<submission_id> <postId>', views.submission_edit, name="submission_edit"),
    path('commission_quit/<int:post_id>', views.commission_quit, name="commission_quit"),
    path('performing_end/<str:profile_id>', views.performing_end, name="performing_end"),
    path('commission_end/<str:profile_id>', views.commission_end, name="commission_end"),

]


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dissatisfication/',views.dissatisfication,name='dissatisfication'),
    path('requisition/<int:complaint_id>',views.requisition,name='requisition'),
    path('announcement_board/',views.announcement_board,name='announcement_board'),
    path('new_announcement/',views.new_announcement,name='new_announcement'),
    path('create_announcement/',views.create_announcement,name='create_announcement'),
    path('announcement_detail/<int:announcement_id>',views.announcement_detail,name='announcement_detail'),
    path('announce_delete/<int:announcement_id>',views.announce_delete,name='announce_delete'),
    path('announce_edit/<int:announcement_id>',views.announce_edit,name='announce_edit'),
    path('update_announce/<int:announcement_id>',views.update_announce,name='update_announce'),
    path('', views.home, name="home"),

]

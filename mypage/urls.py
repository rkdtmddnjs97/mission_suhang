from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.personal, name="profile"),
    path('commissioned/', views.commissioned, name="commissioned"),
    path('performing/', views.performing, name="performing"),
    path('scrap/', views.scrap, name="scrap"),
    path('editProfile/', views.editProfile, name="editProfile"),
    path('updateProfile/', views.updateProfile, name="updateProfile"),
    path('submit_page/<int:post_id>', views.submit_page, name="submit_page"),
    path('submit_send/<int:post_id>', views.submit_send, name="submit_send"),
    path('submission/<int:post_id>', views.submission, name="submission"),
]


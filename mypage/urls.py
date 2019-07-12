from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name="profile"),
    path('commissioned/', views.commissioned, name="commissioned"),
    path('performing/', views.performing, name="performing"),
    path('scrap/', views.scrap, name="scrap"),
    path('editProfile/', views.editProfile, name="editProfile"),
]

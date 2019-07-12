from django.urls import path
from . import views

urlpatterns =[

    path('read/',views.read,name="home1"),
    path('',views.welcome,name="welcome"),
    path('newblog/',views.create,name='newblog'),
    path('update/<int:pk>',views.update,name='update'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('blog/<int:pk>',views.detail,name='detail'),

]
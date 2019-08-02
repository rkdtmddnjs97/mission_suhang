from django.urls import path
from . import views

urlpatterns =[

    path('read/',views.read,name="home1"),
    path('',views.welcome,name="welcome"),
    path('newblog/',views.create,name='newblog'),
    path('update/<int:pk>',views.update,name='view_update'),
    path('delete/<int:pk>',views.delete,name='view_delete'),
    path('blog/<int:pk>',views.detail,name='view_detail'),
    path('new_comment/<int:pk>', views.new_comment, name="view_new_comment"),
    path('scrap/<int:pk>', views.scrap, name="view_scrap"),

]
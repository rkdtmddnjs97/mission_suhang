from django.urls import path
from . import views

urlpatterns =[

    path('read/',views.read,name="home1"),
    path('',views.welcome,name="welcome"),
    path('newblog/',views.create,name='newblog'),
    path('update/<int:pk>',views.update,name='update'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('blog/<int:pk>',views.detail,name='detail'),
<<<<<<< HEAD
    path('new_comment/<int:pk>', views.new_comment, name="new_comment"),
=======
    path('scrap/<int:pk>', views.scrap, name="scrap"),
>>>>>>> 79cf8ac880b116c1fdcc5e123155b81035d6457d

]
from django.contrib import admin
from django.urls import path
import freeBoard.views

urlpatterns = [
  
    path('board/', freeBoard.views.board, name="board"),
    path('post/<int:post_id>', freeBoard.views.detail, name="b_detail"),
    path('new/', freeBoard.views.new, name='b_new'),
    path('create/', freeBoard.views.create, name='b_create'),
    path('edit/<int:post_id>', freeBoard.views.edit, name="b_edit"),
    path('update/<int:post_id>', freeBoard.views.update, name="b_update"),
    path('delete/<int:post_id>', freeBoard.views.delete, name="b_delete"),
    path('new_comment/<int:post_id>', freeBoard.views.new_comment, name="b_new_comment"),
    path('like/<int:post_id>', freeBoard.views.like, name="b_like"),
   
]

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
    path('comment_delete/<int:comment_id>', freeBoard.views.comment_delete, name="b_comment_delete"),
    path('modify/<int:comment_id>', freeBoard.views.modify, name="b_modify"),
    path('like/<int:post_id>', freeBoard.views.like, name="b_like"),
    path('tag_post/<int:tag_id>', freeBoard.views.tag_post, name="b_tag_post"),
    path('like_more/<int:post_id>', freeBoard.views.like_more, name='like_more'),
]

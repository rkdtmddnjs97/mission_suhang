from django.urls import path
from . import views
urlpatterns = [

    path('',views.request_home,name="request"),
    path('<int:post_id>/', views.detail, name="detail"),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('edit/<int:post_id>', views.edit, name="edit"),
    path('update/<int:post_id>', views.update, name="update"),
    path('delete/<int:post_id>', views.delete, name="delete"),
    path('new_comment/<int:post_id>', views.new_comment, name="new_comment"),
    path('scrap/<int:post_id>', views.scrap, name="scrap"),
    path('start/<post_id> <app_id>', views.start, name="start"),
    path('end/<int:post_id>', views.end, name="end"),
    path('comment_delete/<int:comment_id>', views.comment_delete, name="comment_delete"),
    path('modify/<int:comment_id>', views.modify, name="modify"),
    path('tag_post/<int:tag_id>', views.tag_post, name="tag_post"),
    path('missionApply/<int:post_id>', views.apply, name="missionApply"),
      
]

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dissatisfication/',views.dissatisfication,name='dissatisfication'),
    path('requisition/<int:complaint_id>',views.requisition,name='requisition'),
]

"""missionProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import main.views
import view_request.urls
import view_request.views
import request.urls
import search.views
import notification.views
import hashtag.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.home, name="home"),
    path('mypage/', include('mypage.urls')),
    path('accounts/', include('accounts.urls')),
    path('crud/',include(view_request.urls)),
    path('freeBoard/',include('freeBoard.urls')),
    path('request/', include('request.urls')),
    path('search_result/', search.views.search, name="search"),
    path('notifications/', notification.views.notifications, name="notifications"),
    path('notifications/delete/<int:notification_id>', notification.views.delete_notification, name="delete_notification"),
    path('main/', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


   

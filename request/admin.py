
from django.contrib import admin

from .models import Post,Comment, ApplyMission,Hashtag




# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)

admin.site.register( ApplyMission)

admin.site.register(Hashtag)


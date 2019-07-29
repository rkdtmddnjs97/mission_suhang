from django.shortcuts import render
from request.models import Post
# Create your views here.
def home(request):
    completed_posts = Post.objects.filter(status='completed')
    mission_completed = completed_posts.count()
    return render(request, 'home.html',{'mission_completed':mission_completed})
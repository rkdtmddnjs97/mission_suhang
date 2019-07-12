from django.shortcuts import render

# Create your views here.

def profile(request):
    return render(request, 'profile.html')

def commissioned(request):
    return render(request, 'commissioned.html')

def performing(request):
    return render(request, 'performing.html')

def scrap(request):
    return render(request, 'scrap.html')
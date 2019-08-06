from django.shortcuts import render
from .models import Hashtag

# Create your views here.
def hashtag_search_page(request):

    search_data = request.POST['search_tag_data']
    all_tag = Hashtag.objects.all()
    result_tag = []
    for tag in all_tag:
        if search_data in tag.name:
            result_tag.append(tag)

    return render(request,'hashtag_search_page.html', {'result_tag':result_tag})

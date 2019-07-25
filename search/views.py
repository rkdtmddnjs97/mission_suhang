from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from hashtag.models import Hashtag
from request.models import Post


def search(request):
    input_data = request.GET['input_data'].upper()
    try:
        tag = Hashtag.objects.get(name=input_data)
        results = Post.objects.filter(hashtag=tag)
        result_flag = True
        return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag})

    except ObjectDoesNotExist:
        results = '검색 결과가 없습니다^^'
        result_flag = False
        return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag})

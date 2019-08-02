from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from hashtag.models import Hashtag
from request.models import Post
from django.contrib.auth.models import User
from freeBoard.models import B_Blog
from accounts.models import Profile


def search(request):
    input_data = request.GET['input_data']
    input_type = request.GET['input_type']
    input_board = request.GET['input_board']
    if input_board == 'missionboard':
          if input_type == 'hashtag':
               try:
                   tag = Hashtag.objects.get(name=input_data.upper())
                   results = Post.objects.filter(hashtag=tag)
                   input_data = '#'+input_data
                   search_type = 'HashTag'
                   result_flag = True
                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag, 'search_type ':search_type,'input_board':input_board })

               except ObjectDoesNotExist:
                   results = '검색 결과가 없습니다^^'
                   result_flag = False
                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag})
          elif input_type == 'writer':
               try:
                #  user = Profile.objects.get(profile_id=input_data)
                   results = Post.objects.filter(writer=input_data)
                   search_type = 'writer'
                   result_flag = True
                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag, 'search_type ':search_type ,'input_board':input_board})

               except ObjectDoesNotExist:
                  results = '검색 결과가 없습니다^^'
                  result_flag = False
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag})
          elif input_type == 'title':
               try:
                  results = Post.objects.filter(title=input_data)
                  search_type = 'Title'
                  result_flag = True
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag , 'search_type ':search_type,'input_board':input_board })

               except ObjectDoesNotExist:
                  results = '검색 결과가 없습니다^^'
                  result_flag = False
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag})
    
          elif input_type == 'body':
               try:
                   results=[]     
                   search_type = 'Context'
                   result_flag = True
                   for post in Post.objects.all():
                        if input_data in post.body:
                             results.append(post)

                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag, 'search_type ':search_type ,'input_board':input_board})

               except ObjectDoesNotExist:
                    results = '검색 결과가 없습니다^^'
                    result_flag = False
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag})
    elif input_board=="freeboard":
          if input_type == 'hashtag':
               try:
                   tag = Hashtag.objects.get(name=input_data.upper())
                   results = B_Blog.objects.filter(hashtag=tag)
                   input_data = '#'+input_data
                   search_type = 'HashTag'
                   result_flag = True
                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag, 'search_type ':search_type ,'input_board':input_board})

               except ObjectDoesNotExist:
                  results = '검색 결과가 없습니다^^'
                  result_flag = False
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag })
          elif input_type == 'writer':
               try:
                #  user = Profile.objects.get(profile_id=input_data)
                   results = B_Blog.objects.filter(writer=input_data)
                   search_type = 'writer'
                   result_flag = True
                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag, 'search_type ':search_type ,'input_board':input_board })

               except ObjectDoesNotExist:
                  results = '검색 결과가 없습니다^^'
                  result_flag = False
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag })
          elif input_type == 'title':
               try:
                  results = B_Blog.objects.filter(title=input_data)
                  search_type = 'Title'
                  result_flag = True
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag , 'search_type ':search_type ,'input_board':input_board })

               except ObjectDoesNotExist:
                  results = '검색 결과가 없습니다^^'
                  result_flag = False
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag})
    
          elif input_type == 'body':
               try:
                   results=[]     
                   search_type = 'Context'
                   result_flag = True
                   for post in B_Blog.objects.all():
                        if input_data in post.body:
                             results.append(post)

                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag, 'search_type ':search_type ,'input_board':input_board })

               except ObjectDoesNotExist:
                    results = '검색 결과가 없습니다^^'
                    result_flag = False
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag':result_flag })


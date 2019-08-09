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
     search_type = request.GET['search_type']

     if search_type == 'missionboard':

          if input_type == 'hashtag':
               try:
                   tag = Hashtag.objects.get(name=input_data.upper())
                   results = Post.objects.filter(hashtag=tag)
                   input_data = '#'+input_data
                   search_type = 'HashTag'
                   result_flag = True
                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type ': search_type, 'search_type': search_type})

               except ObjectDoesNotExist:
                   results = '검색 결과가 없습니다^^'
                   result_flag = False
                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

          elif input_type == 'writer':
               try:
                #  user = Profile.objects.get(profile_id=input_data)
                   results = Post.objects.filter(writer=input_data)
                   search_type = 'writer'
                   result_flag = True
                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type ': search_type, 'search_type': search_type})

               except ObjectDoesNotExist:
                  results = '검색 결과가 없습니다^^'
                  result_flag = False
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

          elif input_type == 'title':
               try:
                    search_type = 'Title'
                    result_flag = True
                    results = []
                    for post in Post.objects.all():
                         if input_data in post.title:
                              results.append(post)

                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type ': search_type, 'search_type': search_type})
               except ObjectDoesNotExist:
                  results = '검색 결과가 없습니다^^'
                  result_flag = False
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

          elif input_type == 'body':
               try:
                   results = []
                   search_type = 'Context'
                   result_flag = True
                   for post in Post.objects.all():
                        if input_data in post.body:
                             results.append(post)

                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type ': search_type, 'search_type': search_type})
               except ObjectDoesNotExist:
                    results = '검색 결과가 없습니다^^'
                    result_flag = False
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

     elif search_type == "freeboard":
          if input_type == 'hashtag':
               try:
                   tag = Hashtag.objects.get(name=input_data.upper())
                   results = B_Blog.objects.filter(hashtag=tag)
                   input_data = '#'+input_data
                   search_type = 'HashTag'
                   result_flag = True
                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type ': search_type, 'search_type': search_type})
               except ObjectDoesNotExist:
                  results = '검색 결과가 없습니다^^'
                  result_flag = False
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

          elif input_type == 'writer':
               try:
                #  user = Profile.objects.get(profile_id=input_data)
                   results = B_Blog.objects.filter(writer=input_data)
                   search_type = 'writer'
                   result_flag = True
                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type ': search_type, 'search_type': search_type})
               except ObjectDoesNotExist:
                  results = '검색 결과가 없습니다^^'
                  result_flag = False
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

          elif input_type == 'title':
               try:
                  results = B_Blog.objects.filter(title=input_data)
                  search_type = 'Title'
                  result_flag = True
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type ': search_type, 'search_type': search_type})
               except ObjectDoesNotExist:
                  results = '검색 결과가 없습니다^^'
                  result_flag = False
                  return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

          elif input_type == 'body':
               try:
                   results = []
                   search_type = 'Context'
                   result_flag = True
                   for post in B_Blog.objects.all():
                        if input_data in post.body:
                             results.append(post)
                   return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type ': search_type, 'search_type': search_type})
               except ObjectDoesNotExist:
                    results = '검색 결과가 없습니다^^'
                    result_flag = False
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

     elif search_type == "allBoard":
          if input_type == 'hashtag':
               try:
                    tag = Hashtag.objects.get(name=input_data.upper())
                    free_results = B_Blog.objects.filter(hashtag=tag)
                    request_results = Post.objects.filter(hashtag=tag)
                    results = []
                    for f_post in free_results:
                         results.append(f_post)
                    for m_post in request_results:
                         results.append(m_post)

                    input_data = '#'+input_data
                    search_type = 'HashTag'
                    result_flag = True
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type ': search_type, 'search_type': search_type})
               except ObjectDoesNotExist:
                    results = '검색 결과가 없습니다^^'
                    result_flag = False
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

          elif input_type == 'writer':
               try:
                #  user = Profile.objects.get(profile_id=input_data)
                    free_results = B_Blog.objects.filter(writer=input_data)
                    request_results = Post.objects.filter(writer=input_data)
                    results = []
                    for f_post in free_results:
                         results.append(f_post)
                    for m_post in request_results:
                         results.append(m_post)

                    search_type = 'writer'
                    result_flag = True
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type ': search_type, 'search_type': search_type})
               except ObjectDoesNotExist:
                    results = '검색 결과가 없습니다^^'
                    result_flag = False
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

          elif input_type == 'title':
               try:
                    free_results = B_Blog.objects.filter(title=input_data)
                    request_results = Post.objects.filter(title=input_data)
                    results = []
                    for f_post in free_results:
                         results.append(f_post)
                    for m_post in request_results:
                         results.append(m_post)

                    search_type = 'Title'
                    result_flag = True
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type': search_type })
               except ObjectDoesNotExist:
                    results = '검색 결과가 없습니다^^'
                    result_flag = False
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

          elif input_type == 'body':
               try:
                    results = []
                    search_type = 'Context'
                    result_flag = True
                    for post in B_Blog.objects.all():
                         if input_data in post.body:
                              results.append(post)

                    for post in Post.objects.all():
                         if input_data in post.body:
                              results.append(post)

                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type': search_type})
               except ObjectDoesNotExist:
                    results = '검색 결과가 없습니다^^'
                    result_flag = False
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

     elif search_type == "user":
          if input_type == 'user':
               try:
                    results = Profile.objects.filter(profile_id=input_data)
                    search_type = 'user'
                    result_flag = True

                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag, 'search_type': search_type})
               except ObjectDoesNotExist:
                    results = '검색 결과가 없습니다^^'
                    result_flag = False
                    return render(request, 'search_result.html', {'input_data': input_data, 'results': results, 'result_flag': result_flag})

from django.shortcuts import render, get_object_or_404
from blog.models import Blog

def blog_list(request):
    blogs = Blog.objects.all()
    
    # 이렇게 하면 blog 리스트 안에서 문자열로 이미 합쳐서 /blog/로 갔을 때 결과가 시간.315589+00:00 이런식으로 나옴
    # blog = [f'{blog.title} - {blog.created_at}' for blog in blogs] (X)

    # get('visits', 0) => visits의 값을 가져오고, None이라면 0
    # visits가 없는 경우 => 처음 방문한 사용자
    visits = int(request.COOKIES.get('visits', 0)) + 1  # => 방문자 횟수 1 증가 (쿠키)

    request.session['count'] = request.session.get('count', 0) + 1

    context = {
        'blogs': blogs,
        'count': request.session['count']
    }

    response = render(request, 'blog_list.html', context)
    response.set_cookie('visits', visits)   # 위에서 1증가시킨 visits를 response객체의 쿠키에 저장

    return response

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)

    # if blog.valid():
    #     blog.save()
    #     return render(request, 'blog_detail.html')
    # else:
    #     form = Blog.forms()
    # return render(request, 'blog_detail')

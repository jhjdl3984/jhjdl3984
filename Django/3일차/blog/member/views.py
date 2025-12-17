from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings    # => 이렇게 불러오면 나중에 config폴더명 or settings파일명이 바껴도 알아서 찾아서 가져옴
from django.contrib.auth import login as django_login   # 함수도 login이여서 as명으로 만들어주기
from django.urls import reverse

def sign_up(request):
    # username = request.POST.get('username')
    # password1 = request.POST.get('password1')
    # password2 = request.POST.get('password2')

    # print('username', username)
    # print('password1', password1)
    # print('password2', password2)

    # 밑에 주석처럼 if, else 안쓰고 단순화
    # UserCreationForm => django에서 기본 제공해주는 회원가입 관련된 폼
    form = UserCreationForm(request.POST or None)   # => POST요청이면 폼에 post데이터 들어가고, 아닐때(GET요청)는 None

    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    # if request.method == "POST":
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/accounts/login/')
    # else:
    #     form = UserCreationForm()
        
    context = {
            'form': form
        }
    
    # post요청인데 form.is_valid() == false 
    # => 브라우저에서 다시 렌더링될 때, 일반 텍스트인 아이디는 입력값이 그대로 남고, 비밀번호는 보안상 없어짐
    return render(request, 'registration/signup.html', context)

def login(request):
    # AuthenticationForm => django에서 기본 제공해주는 회원가입 관련된 폼
    # POST 요청한 브라우저의 요청정보(쿠키, 세션 등)를 authenticate() 호출 시에 같이 전달
    form = AuthenticationForm(request, request.POST or None)

    if form.is_valid():

        # sign_up처럼 valid하고나서 save할 필요없이 로그인 진행
        # 위의 request와 여기의 reqest는 같음
        # 인증된 객체(form.get_user())를 request에 포함된 쿠키, 세션 등 중에서 세션에 로그인 상태로 연결함
        django_login(request, form.get_user())

        # reverse => 템플릿에서 url을 name으로 찾는것 처럼 얘도 urls에 등록한 name으로 url을 찾음
        # redirect => reverse에서 찾은 url로 이동시켜줌
        return redirect(reverse('blog_list'))

    context = {
        'form': form
    }

    return render(request, 'registration/login.html', context)



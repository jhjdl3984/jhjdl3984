from flask import render_template, request, redirect, url_for, flash
from models import User, users  # users => models.py에서 만든 users 변수
from flask_login import login_user, logout_user, login_required


# 라우트 정의를 따로 모아두기 위해 함수 안에서 app.route를 사용
def configure_route(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    # /login 페이지에 처음 들어오면 => 맨밑에 있는 login.html를 보여줌
    @app.route('/login', methods=["GET", "POST"])
    def login():
        if request.method == "POST":    # 로그인 폼을 제출할 때
            username = request.form["username"]
            password = request.form["password"]

            # models.py에서 User클래스의 함수 get(user_id)
            # => user_id 파라미터에 사용자가 입력한 username을 전달
            user = User.get(username)

            # [username] => 위의 변수 username
            # 예) username = "admin"
            # => users["admin"]['password'] => "pw123"
            if user and users[username]['password'] == password:
                # 세션에 user_id를 넣는 역할
                login_user(user)

                # 로그인 성공하면 index() 함수의 url인 '/'로 이동
                return redirect(url_for('index'))
            # 폼에 입력한 "username"의 유저가 users안에 없는 유저이거나 패스워드가 틀렸을 때
            else:
                flash("Invalid username or password")
        
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        # Flask-Login에서 제공하는 함수 => 현재 로그인되어 있는 사용자 정보를 세션에서 제거 (로그아웃 처리)
        logout_user()
        return redirect(url_for('index'))

    @app.route('/protected')

    # 로그인한 사용자만 접근할 수 있는 페이지를 만들 때 사용
    # 사용자가 로그인 되어있는지 검사
    # 로그인 O => 함수 실행 
    # 로그인 X => login_view로 자동 redirect (app.py에서 login_manager.login_view = "login")
    # => 로그인 안되어 있으면 /login으로 자동으로 보내짐
    @login_required

    def protected():
        return "<h1>Protected area</h1> <a href='/logout'>Logout</a>"

# session => 로그인 상태를 유지하기 위한 작은 저장소
from flask import Flask, render_template, request, redirect, session, flash
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "flask-secret-key" # 실제로 배포시에는 .env or yaml로 ! (털릴 위험 때문)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)    # 세션 유지 기간

# admin user
users = {
    "john": "pw123",
    "leo": "pw123"
}

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username in users and users[username] == password:
        # seesion이라는 dict안에 "username"이라는 키를 만들고 위에서 만든 username인 값을 value로 만든다
        session["username"] = username
        session.permanent = True    # 세션 유지기간 활성화

        # redirect() => 사용자를 다른 URL로 이동시키는 함수
        # => 로그인 성공하면 /secret 페이지로 이동
        return redirect('/secret')
    else:
        # flash() => 보여줄 메세지를 한번만 보여주고 사라짐
        flash("Invalid username or password")
        return redirect('/')    # 다시 '/' 페이지로 돌아감

@app.route('/secret')
def secret():
    if "username" in session:
        return render_template("secret.html")
    # 로그인 안한 사용자가 직접 /secret URL을 입력해서 접근 할 수 있기 때문에 else 필요
    else:
        return redirect('/')
    
@app.route('/logout')
def logout():
    # "username"이 있으면 해당 키와 값을 삭제하고 값 반환 / 없으면 None 반환만
    session.pop("username", None)
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
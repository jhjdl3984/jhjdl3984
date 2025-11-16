from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth   # pip install flask-httpauth

app = Flask(__name__)
auth = HTTPBasicAuth()     # auth => 인증 관련 기능 제공 객체

users = {
    "admin":"secret",
    "guest":"pw123"
}
# HTTP Basic 인증이 필요할 때 verify_password 함수로 username/password 검증해라
@auth.verify_password

def verify_password(username, password):    # 클라이언트가 username, password를 보내면 이 함수가 호출
    if username in users and users[username] == password:
        return username

@app.route('/')
def index():
    return render_template('index.html')

# 1. 사용자가 /protected URL로 요청 => Flask가 연결된 함수 protected()를 호출하려함
@app.route('/protected')

# 2. 호출 전, 이 데코레이터가 먼저 실행 => 로그인 여부 확인(사용자 인증 요구)
@auth.login_required
def protected():
    return render_template('secret.html')

if __name__ == "__main__":
    app.run(debug=True)
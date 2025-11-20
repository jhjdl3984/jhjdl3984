from flask import Flask
from flask_login import LoginManager    # LoginManager => Flask에서 로그인 인증 기능을 제공
from models import User

app = Flask(__name__)
app.secret_key = "Flask-secret-key" # 세션 쿠키 암호화에 쓰이는 비밀키

login_manager = LoginManager()
login_manager.init_app(app) # LoginManager을 Flask 앱에 등록 => 안하면 Flask-Login이 완전 비활성화됨
login_manager.login_view = "login"  # 로그인 안된 상태에서 접근 시 이동시킬 페이지의 이름

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# routes.py에 정의된 모든 route를 Flask 앱에 등록
# => app.py에서는 앱 초기화만 하고 라우트는 따로 관리 할 수 O
from routes import configure_route
configure_route(app)

if __name__ == "__main__":
    app.run(debug=True)

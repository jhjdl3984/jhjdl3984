from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from db import db
from flask_migrate import Migrate

app = Flask(__name__)

# 데이터베이스 및 JWT 설정
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"  # 서버 실행 => app.db가 생성됨
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["API_TITLE"] = 'Todo API'
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"

# db = SQLAlchemy(app) => blueprint 안쓸 때 적합
# db.py에서 db = SQLAlchemy() + app.py에서 db.init_app(app) 
# => DB 객체 생성 + Flask 앱과 DB 연결
db.init_app(app)

# Migrate(app, db) => app과 db를 Flask-Migrate에 연결 (app과 db의 Migrate 기능을 활성화)
# => flask db init, flask db migrate, flask db upgrade 명령어로 DB스키마 버전 관리 O
migrate = Migrate(app, db)

jwt = JWTManager(app)   # JWT 관련 기능을 Flask 앱과 연결
api = Api(app)

# 모델 및 리소스 불러오기 (이후에 정의)
from models import User, Todo
from routes.auth import auth_blp
from routes.todo import todo_blp

# API에 Blueprint 등록
api.register_blueprint(auth_blp)
api.register_blueprint(todo_blp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
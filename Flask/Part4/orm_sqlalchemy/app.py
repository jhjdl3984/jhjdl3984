from flask import Flask
from flask_smorest import Api
from db import db
from models import User, Board  # modles.py에 있는 User클래스, Board클래스를 현재 파일로 가져옴
from flask_migrate import Migrate

app = Flask(__name__)

# SQLAlchemy를 통해 데이터베이스에 접속할 수 있는 명령어
# "SQLAlCHEMY_DATABASE_URI" => SQLAlchemy가 사용할 db주소를 의미
# db종류+python드라이버://db사용자이름:비번/db서버주소/db이름
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:0000@localhost/oz"

# flask-SQLAlchemy => 모든 객체 변경 사항을 추적하려 함 => False로 꺼줌 (메모리와 성능 낭비문제때문)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db.py에서 db = SQLAlchemy()로 만든 db가 app과 실제 DB에 연결됨
db.init_app(app)

# Migrate 객체 생성하고 Flask app 및 SQLAlchemy 데이터베이스 인스턴스(db)와 연결
migrate = Migrate(app, db)

# blueprint 설정
# Swagger / OpenAPI => API 문서를 자동으로 만들어주는 틀
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.3"

# Swagger UI가 OPENAPI_URL_PREFIX에 있는 json 설계도를 가져와서 /swagger-ui 페이지에 이쁘게 그려주는 것
app.config["OPENAPI_URL_PREFIX"] = "/"  # Swagger UI가 "/openapi.json"을 읽음
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"   # 사용자가 들어가는 웹 주소

# Swagger UI가 필요로 하는 JS/CSS 파일을 어디서 불러올지 결정 (CDN => 외부 서버에서 파일을 빠르게 제공)
app.config["OPENAPI_SWAGGER_UI_URL"] = "http://cdn.jsdelivr.net/npm/swagger-ui-dist/" 

# Flask 앱과 Swagger가 연결됨
api = Api(app)


# api(Api 객체)에 blueprint를 등록
from routes.board import board_blp
from routes.user import user_blp
api.register_blueprint(board_blp)
api.register_blueprint(user_blp)

from flask import render_template
# /manage-boards 경로로 가면 => boards.html 파일을 보여줌
@app.route('/manage-boards')
def manage_boards():
    return render_template("boards.html")

@app.route('/manage-users')
def manage_users():
    return render_template('users.html')

# 다른 파일에서 import app으로 실행하면 위에 코드들만 실행되고 이 if문은 실행 X
# 오직 이 파일에서 실행했을 때만 실행됨
if __name__ == "__main__":
    # Flask는 DB작업 등을 하기 위해 app_context라는 실행환경이 필요
    with app.app_context(): # app_context => Flask 앱 활성화
        db.create_all() # DB 연결이 필요한 작업
    app.run(debug=True)



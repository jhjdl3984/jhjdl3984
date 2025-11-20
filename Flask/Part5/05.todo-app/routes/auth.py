from flask import request, jsonify
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token
from models import User
from werkzeug.security import check_password_hash

auth_blp = Blueprint("auth", "auth", url_prefix="/login", description="Operations on todos")

@auth_blp.route('/', methods=["POST"])
def login():
    # request.is_json => 요청이 JSON 형식인지 확인하는 용도
    if not request.is_json:
        print("if not request.is_josn")
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    # request.json => 요청 본문(JSON)을 python dict로 변환
    # .get("username") => dict에서 "username" 키의 값을 가져옴
    # request.json["username"] == request.json.get("username")
    # => []로 접근하면 키가 없을 때 에러 발생 / .get()로 접근하면 None 반환
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        print("if not username or not password")
        return jsonify({"msg": "Missing username or password"}), 400
    
    # User 테이블에서 username이 입력한 username의 값과 일치하는 행을 찾고 그 중 첫 번째 사용자 객체
    # User.query.filter_by(username=username)
    # => <flask_sqlalchemy.BaseQuery object at 0x...> 이런식으로 쿼리 객체 반환됨
    user = User.query.filter_by(username=username).first()

    print("user 여기는오나", user)
    print("user 여기는오나", check_password_hash(user.password_hash, password))

    if user and check_password_hash(user.password_hash, password):
        # identity => JWT 토큰 안에 어떤 사용자 정보를 넣을 것인지 정하는 옵션
        # identity=username => 로그인한 사용자 이름을 토큰 내부에 저장
        # => {"sub": "leo"} 이런식으로 JWT 토큰 안에 저장됨
        access_token = create_access_token(identity=username)
        print("access token", access_token)

        # 예) {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI..."}
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad username or password"}), 401
from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models.user import User

user_bp = Blueprint('user', __name__)

# 임시 사용자 데이터
users = {
    'user1': User('1', 'user1', 'pw123'),
    'user2': User('2', 'user2', 'pw123')
}

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 여기에선 새로운 사용자 추가 X => 기존 사용자 정보와 비교해서 맞으면 로그인 처리
    if request.method == 'POST':
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        user = users.get(username)
        if user and user.password == password:
            # 로그인한 사용자의 identity를 넣어서 엑세스 토큰 생성
            access_token = create_access_token(identity=username)
            # 동일한 사용자의 리프레시 토큰 생성
            refresh_token = create_refresh_token(identity=username)
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        else:
            return jsonify({"msg": "Bad username or password"}), 401
    else:
        return render_template('login.html')


@user_bp.route('/protected', methods=['GET'])
@jwt_required() # 요청에 유효한 JWT 토큰이 접근했는지 => 인증된 유저인지 아닌지
def protected():
    # get_jwt_identity() => JWT 토큰의 identity값을 가져옴
    # 예) 로그인할 때 create_access_token(identity=username)으로 토큰을 만들었으면 username이 반환됨
    # => 누가 요청했는지 알아내는 역할
    current_user = get_jwt_identity()
    # 예) username이 user1이면 {"logged_in_as": "usr1"}
    return jsonify(logged_in_as=current_user), 200

@user_bp.route('/protected_page')
def protected_page():
    return render_template('protected.html')

from flask_jwt_extended import get_jwt
from blocklist import add_to_blocklist  # 블랙리스트 관리 모듈 임포트
@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # get_jwt() => 현재 요청에서 사용된 JWT 토큰의 내용(payload) 전체를 딕셔너리 형태로 가져옴
    # ["jti"] => 그 안에 "jti"라는 키의 값(JWT 토큰 고유 ID)
    jti = get_jwt()["jti"]
    add_to_blocklist(jti)  # jti를 블랙리스트에 추가
    return jsonify({"msg": "Successfully logged out"}), 200
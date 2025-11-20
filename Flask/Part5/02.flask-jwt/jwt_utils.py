# JWTManager => JSON Web Token을 관리하기 위한 객체(로그인,인증 등)
# JWT를 이용하면 서버가 세션 없이도 사용자를 인증할 수 O
# JWT => 토큰 자체
from flask_jwt_extended import JWTManager   # pip install flask-jwt-extended

from blocklist import BLOCKLIST
from flask import jsonify

jwt = JWTManager()

# Flask 앱을 받아서 JWT 관련 설정을 한번에 모아서 처리하는 함수
def configure_jwt(app):
    # 서버만 알고 있어야 하며, 토큰 변조 방지를 위해 사용함
    # 예) 토큰 => eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9  => HEADER(어떤 알고리즘으로 서명했는지의 정보)
    #            .                                     => .으로 나눔
    #           eyJ1c2VyX2lkIjoxMjMsIm5hbWUiOiJKb2huIn0 => PAYLOAD(사용자 정보, 권한 등)
    #            .
    #           sflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c => SIGNATURE(HEADER + PAYLOAD + SECRET_KEY의 해시값)
    # HEADER, PAYLOAD => 누구나 볼 수 O / SIGNATURE => SECRET_KEY 없이는 생성, 검증 X

    # SIGNATURE은 HEADER + PAYLOAD + SECRET_KEY로 만든 해시값이기 때문에,
    # 누군가 HEADER나 PAYLOAD를 바꾸면
    # => 서버가 SECRET_KEY를 이용해 새로 계산한 SIGNATURE와 토큰 안의 원래 SIGNATURE가 다르기 때문에
    #    토큰이 변조됐다고 판단할 수 O
    # SIGNATURE => 토큰이 발급 이후 바뀌지 않았음을 보장하는 안전장치
    app.config["JWT_SECRET_KEY"] = "jwt_secret_key"

    # 토큰 만료 시간 설정
    # JWT_ACCESS_TOKEN_EXPIRES 설정 값 => 초단위
    freshness_in_minutes = 60   # 60분
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = freshness_in_minutes * 60 # 3600초
    jwt.init_app(app)

    # claim => JWT PAYLOAD에 들어가는 정보
    # 추가적인 정보를 토큰에 넣고 싶을 때 사용
    @jwt.additional_claims_loader

    def add_claims_to_jwt(identity):
        # identity가 1이면 관리자로 표시
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}  # 일반사용자 표시

    # 토큰이 블록리스트에 있는지 확인하는 함수
    # 블록리스트에 있으면 해당 토큰이 유효하지 않다고 판단
    @jwt.token_in_blocklist_loader

    # Flask-JWT-Extended는 무조건 함수를 호출할 때 header와 payload 두개를 보냄 => 파라미터도 2개 필요함
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        # True반환 => 차단된 토큰으로 판단하고 접근 거부
        # False반환 -> 접근 가능
        return jwt_payload["jti"] in BLOCKLIST

    # 만료된 토큰이 사용되었을 때 실행되는 함수
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"msg": "Token expired", "error": "token_expired"}), 401

    # 유효하지 않은 토큰이 사용되었을 때 실행되는 함수
    # 토큰의 서명이나 구조가 유효하지 않을 때 실행됨. 주로 토큰 자체의 문제로 발생하는 경우
    # 1. HEADER.PAYLOAD.SIGNATURE 형태가 아닐 때
    # 2. 누군가 토큰을 조작했을 때
    # 3. 토큰이 비어있을 때
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Invalid token", "error": "invalid_token"}
            ),
            401
        )

    # 해당 토큰으로 접근 권한이 없는 경우
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Access token required",
                    "error": "access_token_required",
                }
            ),
            401
        )

    # fresh한 토큰이 필요한데 fresh하지 않은 토큰이 사용되었을 때 실행되는 함수
    # fresh 토큰 => 방금 로그인해서 새로 발급한 토큰
    # => 어제 로그인한 토큰과 오늘 로그인한 토큰이 다름
    # 해당 응답을 반환하여 fresh한 토큰이 필요하다는 메시지를 전달
    # JWT_ACCESS_TOKEN_EXPIRES으로 토큰 만료 시간 조정
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "Token is not fresh.", "error": "fresh_token_required"}
            ),
            401
        )
    # 토큰이 폐기되었을 때 실행되는 함수
    # revoked token => 토큰 자체는 만료되지 않았어도 인위적으로 사용할 수 없게 만든 토큰
    # 예) 사용자가 로그아웃 했을 때, 관리자가 특정 유저를 강제 로그아웃, 보안문제로 토큰 강제 무효화
    # => 어제 로그인했던 브라우저에 저장되어있는 토큰으로 요청 보내면 BLOCKLIST에 있어서 접근 거부
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "Token has been revoked.", "error": "token_revoked"}
            ),
            401
        )